#!/usr/bin/env python3
"""
Categorize Bank of America CSV transactions using simple string rules (no regex authoring).

How it works:
1. Reads your BofA CSV, skipping the summary/header section before actual transactions.
2. Ignores the "Running Balance" column (we only keep Date, Description, Amount).
3. Cleans up the Description text and tries to match it to patterns from rules.json.
4. rules.json only contains plain words/phrases (case and spacing don’t matter).
5. The code auto-builds flexible, case-insensitive regex from those words/phrases.
6. Picks the "most specific" match (longest text span matched) for each transaction.

Usage:
    python categorize.py --csv transactions.csv --rules rules.json --out categorized.csv --preview Food
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd


# ---------------------------
# STEP 1: CSV LOADING
# ---------------------------

def first_txn_row(path: str) -> int:
    """
    Find the first row in the CSV that actually contains a transaction.
    Bank of America CSVs often have summary lines before the header.
    Transactions start with a date like MM/DD/YYYY, in the first column.
    """
    date_start = re.compile(r'^\s*\d{2}/\d{2}/\d{4}\s*,')  # matches e.g., "08/04/2025,"
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if date_start.match(line):
                return i
    return 0  # fallback: start from the top if not found


def load_bofa_csv(path: str) -> pd.DataFrame:
    """
    Load the CSV starting at the first transaction row.
    Keeps only the first 3 columns: Date, Description, Amount.
    """
    start = first_txn_row(path)
    df = pd.read_csv(
        path,
        skiprows=start,      # skip the summary lines and header
        header=None,         # no header since we’re defining columns manually
        dtype=str,
        engine="python"
    )
    # Keep only first 3 cols (ignore Running Balance if present)
    df = df.iloc[:, :3].copy()
    df.columns = ["Date", "Description", "Amount"]
    return df


# ---------------------------
# STEP 2: RULE LOADING
# ---------------------------

def make_loose_regex(term: str) -> re.Pattern:
    """
    Turn a plain string into a flexible, case-insensitive regex:
    - Ignores capitalization (re.I).
    - Treats spaces/dashes/punctuation as interchangeable (\W*).
    - Avoids matching inside larger words (lookarounds).
    """
    # Remove accidental extra spaces from rules.json entries
    term = term.strip()

    # Split into tokens (words) on any non-alphanumeric character
    tokens = [t for t in re.split(r"[^\w]+", term) if t]
    if not tokens:
        # If nothing meaningful, just escape the term literally
        return re.compile(re.escape(term), re.I)

    # Join tokens with \W* to allow flexible separators in matches
    body = r"\W*".join(map(re.escape, tokens))

    # Use lookarounds instead of \b to handle punctuation cleanly
    pattern = rf"(?<![A-Z0-9]){body}(?![A-Z0-9])"
    return re.compile(pattern, re.I)


def load_rules_json(path: str) -> Dict[str, Dict[str, List[re.Pattern]]]:
    """
    Load the rules.json file and compile the plain strings into regex patterns.
    The JSON format should be:
    {
      "Category": {
        "Subcategory": ["Merchant1", "Merchant2", ...],
        ...
      },
      ...
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    compiled: Dict[str, Dict[str, List[re.Pattern]]] = {}
    for category, subs in raw.items():
        compiled[category] = {}
        for subcat, terms in subs.items():
            compiled[category][subcat] = [make_loose_regex(t) for t in terms]
    return compiled


# ---------------------------
# STEP 3: MATCHING LOGIC
# ---------------------------

def best_match(desc: str, rules: Dict[str, Dict[str, List[re.Pattern]]]) -> Tuple[str, str]:
    """
    Try all patterns and return the (category, subcategory) of the 'most specific' hit.
    'Most specific' means: longest matching text span found in the description.
    If no matches are found, returns ("Uncategorized", "Other").
    """
    best_len = -1
    best_pair = ("Uncategorized", "Other")

    for cat, subs in rules.items():
        for sub, patterns in subs.items():
            for pat in patterns:
                m = pat.search(desc)
                if m:
                    span_len = m.end() - m.start()
                    if span_len > best_len:
                        best_len = span_len
                        best_pair = (cat, sub)
    return best_pair


# ---------------------------
# STEP 4: HELPERS
# ---------------------------

def normalize_desc(s: str) -> str:
    """
    Light cleanup of the description:
    - Removes double spaces.
    - Strips leading/trailing whitespace and punctuation.
    """
    s = str(s or "")
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def to_float(x):
    """
    Convert amount string to float.
    Handles commas, dollar signs, and ignores blanks.
    """
    try:
        s = str(x).strip()
        if s == "" or s.lower() in {"nan", "none"}:
            return pd.NA
        return float(s.replace(",", "").replace("$", ""))
    except Exception:
        return pd.NA


def merchant_hint(desc: str) -> str:
    """
    Extract the first few words from description for a quick merchant 'name' column.
    This is purely cosmetic and not used for matching.
    """
    return " ".join(str(desc).split()[:5])


# ---------------------------
# STEP 5: MAIN
# ---------------------------

def main():
    ap = argparse.ArgumentParser(description="Categorize BofA CSV using simple string rules (no regex authoring).")
    ap.add_argument("--csv", required=True, help="Path to BofA CSV export")
    ap.add_argument("--rules", default="rules.json", help="Path to rules.json (strings only)")
    ap.add_argument("--out", default="categorized_transactions.csv", help="Output CSV path")
    ap.add_argument("--preview", default="Food", help="Top-level category to preview in stdout")
    args = ap.parse_args()

    # Load category rules
    rules = load_rules_json(args.rules)

    # Load CSV
    df = load_bofa_csv(args.csv)

    # Clean description and amount
    df["Description"] = df["Description"].astype(str).apply(normalize_desc)
    df["Amount"] = df["Amount"].apply(to_float)

    # Drop non-transaction rows (e.g., Beginning/Ending balance lines inside the table)
    df = df[df["Amount"].notna()].copy()

    # Merchant hint column for human readability
    df["Merchant"] = df["Description"].apply(merchant_hint)

    # Categorize each transaction
    pairs = df["Description"].apply(lambda d: best_match(d, rules))
    df["Category"] = pairs.apply(lambda x: x[0])
    df["Subcategory"] = pairs.apply(lambda x: x[1])

    # Save results
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df[["Date", "Description", "Merchant", "Amount", "Category", "Subcategory"]].to_csv(
        args.out, index=False
    )
    print(f"Wrote {args.out}")

    # Show preview of one category (default: Food)
    subset = df[df["Category"] == args.preview]
    if not subset.empty:
        print(f"\n=== {args.preview.upper()} TRANSACTIONS ===")
        print(subset[["Date", "Merchant", "Amount", "Subcategory"]].to_string(index=False))
    else:
        print(f"\n(No {args.preview} transactions found.)")


if __name__ == "__main__":
    main()
