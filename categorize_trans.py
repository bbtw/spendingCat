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
python categorize_trans.py --transaction_file ~/Downloads/transactions.csv --output_file_name categorized.csv --preview Food

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
    """Find first transaction row in a BofA CSV."""
    date_start = re.compile(r'^\s*\d{2}/\d{2}/\d{4}\s*,')
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            if date_start.match(line):
                return i
    return 0


def load_bofa_csv(path: str) -> pd.DataFrame:
    """Load BofA CSV starting at first transaction row."""
    path = str(Path(path).expanduser())
    start = first_txn_row(path)
    df = pd.read_csv(path, skiprows=start, header=None, dtype=str, engine="python")
    df = df.iloc[:, :3].copy()
    df.columns = ["Date", "Description", "Amount"]
    return df


# ---------------------------
# STEP 2: RULE LOADING
# ---------------------------

def make_loose_regex(term: str) -> re.Pattern:
    """Convert a plain string into a flexible, case-insensitive regex."""
    term = term.strip()
    tokens = [t for t in re.split(r"[^\w]+", term) if t]
    if not tokens:
        return re.compile(re.escape(term), re.I)
    body = r"\W*".join(map(re.escape, tokens))
    pattern = rf"(?<![A-Za-z0-9]){body}(?![A-Za-z0-9])"
    return re.compile(pattern, re.I)


def load_rules_json(path: Path) -> Dict[str, Dict[str, List[re.Pattern]]]:
    """Load rules.json and compile patterns."""
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    compiled: Dict[str, Dict[str, List[re.Pattern]]] = {}
    for category, subs in raw.items():
        compiled[category] = {
            subcat: [make_loose_regex(t) for t in terms]
            for subcat, terms in subs.items()
        }
    return compiled


# ---------------------------
# STEP 3: MATCHING LOGIC
# ---------------------------

def best_match(desc: str, rules: Dict[str, Dict[str, List[re.Pattern]]]) -> Tuple[str, str]:
    """Return (category, subcategory) of most specific match."""
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
    """Light cleanup of description text."""
    s = str(s or "")
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def to_float(x):
    """Convert amount to float, handling commas/dollar signs."""
    try:
        s = str(x).strip()
        if s == "" or s.lower() in {"nan", "none"}:
            return pd.NA
        return float(s.replace(",", "").replace("$", ""))
    except Exception:
        return pd.NA


def merchant_hint(desc: str) -> str:
    """Extract first few words from description for readability."""
    return " ".join(str(desc).split()[:5])


# ---------------------------
# STEP 5: MAIN
# ---------------------------

def main():
    ap = argparse.ArgumentParser(description="Categorize BofA CSV using simple string rules (no regex authoring).")
    ap.add_argument("--transaction_file", required=True, help="Path to BofA CSV export")
    ap.add_argument("--output_file_name", default="categorized_transactions.csv", help="Output CSV path")
    ap.add_argument("--preview", default="Food", help="Top-level category to preview in stdout")
    args = ap.parse_args()

    rules_path = Path(__file__).parent / "rules.json"
    if not rules_path.exists():
        raise FileNotFoundError(f"rules.json not found at {rules_path}. Put it next to main.py.")
    rules = load_rules_json(rules_path)

    df = load_bofa_csv(args.transaction_file)
    df["Description"] = df["Description"].astype(str).apply(normalize_desc)
    df["Amount"] = df["Amount"].apply(to_float)
    df = df[df["Amount"].notna()].copy()
    df["Merchant"] = df["Description"].apply(merchant_hint)

    pairs = df["Description"].apply(lambda d: best_match(d, rules))
    df["Category"] = pairs.apply(lambda x: x[0])
    df["Subcategory"] = pairs.apply(lambda x: x[1])

    Path(args.output_file_name).parent.mkdir(parents=True, exist_ok=True)
    df[["Date", "Description", "Merchant", "Amount", "Category", "Subcategory"]].to_csv(
        args.output_file_name, index=False
    )
    print(f"Wrote {args.output_file_name}")

    subset = df[df["Category"] == args.preview]
    if not subset.empty:
        print(f"\n=== {args.preview.upper()} TRANSACTIONS ===")
        print(subset[["Date", "Merchant", "Amount", "Subcategory"]].to_string(index=False))
    else:
        print(f"\n(No {args.preview} transactions found.)")


if __name__ == "__main__":
    main()
