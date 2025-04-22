### This folder holds the source code for the Glory Days inventory management system.

Here is the file stucture and description of the `src` folder

``` bash
CSC289-Group5-GloryDays/
├── docs/     # Contents excludes for this diagram
├── src/
│   ├── app.py    # This file launches the application
│   ├── db_setup.py    # Sets up databases
│   ├── inventory.db     # Stores inventory data in tables
│   ├── login_database.db     # Stores employee info
│   ├── login.py     # Backend for login and registration
│   ├── README.md     <--- # You are here
│   ├── static/     # Folder for CSS styles and images
│   │   ├── images/     # Folder holding images
│   │   │   └── GloryDaysLogoCircle.JPG     # Glory Days logo
│   │   ├── admin.css     # Style for admin page
|   |   ├── inventory.css     # Style for inventory page
|   |   ├── login.css     # Style for both login and registration pages
|   |   └── sales.css     # Style for sales page
│   └── templates/     # Folder for frontend HTML files
│       ├── admin.html     # Admin page frontend
│       ├── inventory.html     # Inventory frontend
|       ├── login.html     # Login frontend
|       ├── register.html     # Frontend for registration page
|       └── sales.html     # Front end for sales page
```