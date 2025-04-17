# CSC289 Programming Capstone Project

**Project Name:** Glory Days Inventory Management System  
**Team Number:** 5  
**Team Project Manager:** Devin McLoughlin  
**Team Members:** Ryan David McWhirt, Terry Wiggins, Anthony De Casas Mata, Thomas Coates

---

# Software Installation Guide: Glory Days Inventory Management System

## Introduction

The Glory Days Inventory Management System is a Python-based desktop application using Flask designed to assist retail staff in managing inventory, employee accounts, and daily sales at Glory Days, a store specializing in buying and reselling video games. This guide provides detailed instructions for installing, launching, and troubleshooting the system.

---

## System Requirements

- **Operating System:** Windows 10/11, macOS Monterey or later, or Linux (Ubuntu 20.04+ recommended)  
- **Python Version:** Python 3.10 or newer  
- **Hardware Requirements:**
  - Processor: 1 GHz or faster
  - RAM: 4 GB minimum
  - Storage: At least 100 MB of free space
- **Dependencies:** Installed from `requirements.txt`

---

## Downloading the Installer

The project is hosted on GitHub. You can either clone the repository or download the ZIP archive.

### Option 1: Clone from GitHub

```bash
git clone https://github.com/Devin1mc/CSC289-Group5-GloryDays.git
```

### Option 2: Download ZIP

1. Visit: [https://github.com/Devin1mc/CSC289-Group5-GloryDays](https://github.com/Devin1mc/CSC289-Group5-GloryDays)  
2. Click the green **Code** button, then select **Download ZIP**  
3. Extract the ZIP file to a folder of your choice

---

## Installing the Software

1. Open a terminal or command prompt.
2. Navigate to the project directory:

```bash
cd path/to/CSC289-Group5-GloryDays
```

3. *(Optional but recommended)* Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

4. Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Launching the Software

1. Change into the `src` directory:

```bash
cd src
```

2. Launch the application:

```bash
python app.py
```

3. The Flask development server will start, and the app will be hosted locally.
By default, you can open it in your web browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Uninstalling the Software

To uninstall:

1. Delete the project folder.
2. If you created a virtual environment, delete the `venv` folder.
3. No system files are modified, so no further action is required.

---

## Troubleshooting

| Problem | Solution |
|--------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` to install missing packages. |
| Command not recognized | Make sure Python is installed and added to your system's PATH. |
| App won't launch | Confirm you're in the `src` directory and using `python app.py`. |
| Missing database | Ensure `inventory.db` and `login_database.db` are present in the correct locations (In the `src` folder by default). |

---

## Support and Contact Information

- **Email:** [dtmcloughlin@my.waketech.edu](mailto:dtmcloughlin@my.waketech.edu)
- **GitHub Repository:** [https://github.com/Devin1mc/CSC289-Group5-GloryDays](https://github.com/Devin1mc/CSC289-Group5-GloryDays)  
- **Documentation:** [Add link if separate PDF or README exists]
