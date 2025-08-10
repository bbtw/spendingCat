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
After opening the project, create a virtual environment to manage its specific dependencies.

### Prerequisites for Environment Setup
- **Install the Python Extension**: Before you start, make sure you have the official 
[Python extension from Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-python.python) installed in VS Code.

### Steps to Create the Environment
1.  **Open the Command Palette**
    - **Mac**: `Cmd+Shift+P`

2.  **Run the Create Environment Command**
    - Type **`Python: Create Environment`** and select it from the list.

3.  **Select Environment Type**
    - Choose **`Venv`** from the options. This uses Python's built-in tool to create the environment.

4.  **Choose a Python Interpreter**
    - VS Code will show a list of Python versions installed on your system. Select the one you want to use for this project.
    - VS Code will create a `.venv` folder and ask if you want to use this environment for the workspace. Click **Yes**.

### Verify the Setup
- **Terminal**: Open a new terminal (`Terminal > New Terminal`). You should see **`(.venv)`** at the start of the prompt, which confirms the environment is active.
- **Status Bar**: The bottom-right corner of VS Code will now display the Python interpreter from your `.venv`.

---

