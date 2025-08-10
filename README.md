# How to Checkout a Project into VS Code
This guide explains how to clone a Git repository into Visual Studio Code and start working on it.

---

## Prerequisites
1. **Install Git** - Check if Git is installed:  
     ```bash
     git --version
     ```
   - If not installed, download from: [https://git-scm.com/downloads](https://git-scm.com/downloads).

2. **Install Visual Studio Code** - Download from: [https://code.visualstudio.com/](https://code.visualstudio.com/).

---

## Steps to Checkout (Clone) the Project

### 1. Open VS Code
Launch Visual Studio Code on your computer.

---

### 2. Open the Command Palette
- **Mac**: `Cmd+Shift+P`

---

### 3. Start the Clone Command
- Type: `Git: Clone`
- Select it from the dropdown list that appears.

---

### 4. Enter the Repository URL
- Paste the Git repository URL (`https://github.com/bbtw/spendingCat.git`).
- Press `Enter`.

---

### 5. Choose Destination Folder
- Browse and select the folder where you want to save the project.
- VS Code will create a new folder with the repository name inside your chosen location.

---

### 6. Open the Project
- After cloning completes, VS Code will ask: "Would you like to open the cloned repository?"
- Click **"Open"** to start working with the project.

---

## Project Cloned
The project is now cloned to your local machine and open in VS Code. The next step is to set up the Python environment.

## Troubleshooting
- **Authentication required**: VS Code may prompt you to sign in to GitHub.
- **Permission denied**: Make sure you have access to the repository.
- **Git not found**: Ensure Git is properly installed and in your system PATH.

---

## Setting Up the Python Virtual Environment
After opening the project, create a virtual environment using the terminal to manage its specific dependencies.

### Prerequisites for Environment Setup
- **Python Installation**: Ensure Python 3.6 or higher is installed on your system:
  ```bash
  python3 --version
  ```
  If not installed, download from: [https://python.org/downloads](https://python.org/downloads)

### Steps to Create the Environment

1. **Open Terminal in VS Code**
   - Go to `Terminal > New Terminal` or use the shortcut:
     - **Mac**: `Ctrl+`` (backtick)
   - Make sure you're in the project root directory

2. **Create the Virtual Environment**
   ```bash
   python3 -m venv .venv
   ```
   This creates a `.venv` folder containing the isolated Python environment.

3. **Activate the Virtual Environment**
   - **Mac/Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```

4. **Verify Activation**
   After activation, your terminal prompt should show `(.venv)` at the beginning:
   ```bash
   (.venv) your-username@computer:~/path/to/project$
   ```

5. **Install Project Dependencies** (if requirements.txt exists)
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure VS Code to Use the Virtual Environment**
   - Open Command Palette (`Cmd+Shift+P` on Mac)
   - Type `Python: Select Interpreter`
   - Choose the interpreter from `.venv/bin/python` (or `.venv\Scripts\python.exe` on Windows)

### Managing the Environment

- **Deactivate the environment** when you're done working:
  ```bash
  deactivate
  ```

- **Reactivate the environment** when you return to work:
  ```bash
  source .venv/bin/activate  # Mac/Linux
  .venv\Scripts\activate     # Windows
  ```

### Verify the Setup
- **Terminal**: The terminal prompt should show `(.venv)` when the environment is active
- **Status Bar**: The bottom-right corner of VS Code should display the Python interpreter from your `.venv`
- **Check Python path**: Run `which python` (Mac/Linux) or `where python` (Windows) to confirm it points to your virtual environment

---