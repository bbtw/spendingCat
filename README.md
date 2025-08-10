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
- Paste the Git repository URL (e.g., `https://github.com/username/repository-name.git`)
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

## You're Done!
The project is now cloned to your local machine and open in VS Code. You can start editing files, making commits, and pushing changes back to the repository.

---

## Troubleshooting
- **Authentication required**: VS Code may prompt you to sign in to GitHub
- **Permission denied**: Make sure you have access to the repository
- **Git not found**: Ensure Git is properly installed and in your system PATH
