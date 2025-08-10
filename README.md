# How to Checkout a Project into VS Code
This guide explains how to clone a Git repository into Visual Studio Code and start working on it.

---

## Prerequisites
1. **Install Git**  
   - Check if Git is installed:  
     ```bash
     git --version
     ```
   - If not installed, download from: [https://git-scm.com/downloads](https://git-scm.com/downloads).

2. **Install Visual Studio Code**  
   - Download from: [https://code.visualstudio.com/](https://code.visualstudio.com/).

---

## Steps to Checkout (Clone) the Project

### 1. Open VS Code
Launch Visual Studio Code on your computer.

---

### 2. Open the Command Palette
- **Mac**: Press `Cmd+Shift+P`

---

### 3. Start the Clone Command
- Type: `Git: Clone`
- Select it from the dropdown list that appears

---

### 4. Enter the Repository URL
- Paste the Git repository URL -- `https://github.com/bbtw/spendingCat.git`
- Press `Enter`

---

### 5. Choose Destination Folder
- Browse and select the folder where you want to save the project
- VS Code will create a new folder with the repository name inside your chosen location

---

### 6. Open the Project
- After cloning completes, VS Code will ask: "Would you like to open the cloned repository?"
- Click **"Open"** to start working with the project

---

---

## Switching to a Feature Branch

### 1. Open the Source Control Panel
- Click the **Source Control** icon in the left sidebar (looks like a branch)
- Or press `Cmd+Shift+G` (Mac)

---

### 2. View Current Branch
- Look at the bottom-left corner of VS Code
- You'll see the current branch name (usually `main` or `master`)

---

### 3. Switch/Create Branch
- Click on the branch name in the bottom-left corner
- Select one of these options:
  - **"Create new branch..."** - to create a new feature branch
  - **"Switch to another branch..."** - to switch to an existing branch

---

### 4. Name Your Feature Branch
- If creating new: Enter a descriptive name (e.g., `feature/user-login`, `fix/navigation-bug`)
- If switching: Select the branch from the list

---

### 5. Start Coding
- You're now working on your feature branch
- Make your changes and commit them
- Push your branch when ready: `Ctrl+Shift+P` → `Git: Push`

---

## You're Done!
The project is now cloned to your local machine and open in VS Code. You can start editing files, making commits, and pushing changes back to the repository.

---

## Troubleshooting
- **Authentication required**: VS Code may prompt you to sign in to GitHub
- **Permission denied**: Make sure you have access to the repository
- **Git not found**: Ensure Git is properly installed and in your system PATH
