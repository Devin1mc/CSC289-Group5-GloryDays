# CSC289 Programming Capstone Project

**Project Name:** Glory Days Inventory Management System  
**Team Number:** 5  
**Team Project Manager:** Devin McLoughlin  
**Team Members:** Ryan David McWhirt, Terry Wiggins, Anthony De Casas Mata, Thomas Coates

---

## Release Report  
**Glory Days Inventory Management System - Version 1.0**

---

### Overview

The Glory Days Inventory Management System is a web-based application designed for use in a small retail store called "Glory Days" which specializes in buying and reselling video games. This software helps employees and managers track inventory by providing features to add, update, delete, and record sales of games. Managers have access to an administrative portal where they can oversee employee accounts and monitor revenue. All inventory and login data is securely stored in a local database.

This release marks the initial public deployment of the application. It is considered stable, with no known issues at launch.

---

### Development Highlights

#### Project Initiation

The project began with team discussions outlining the goals and scope of the application. Planning sessions focused on identifying core features, user roles, and security requirements.

#### Requirements Gathering

Requirements were gathered through scenario-based brainstorming and evaluation of typical inventory needs for a game retail store. This included role-based permissions, inventory control, and sales tracking.

#### Design and Architecture

The system uses a client-server architecture built on the Flask micro-framework in Python. Flask handles the Python backend logic and routing, while the frontend is developed using HTML, CSS, and JavaScript to provide an intuitive user experience. A local SQLite database is used to store inventory, user accounts, and sales data.

Passwords are hashed using Python’s `hashlib` library for security. The login system enforces secure authentication for both employees and managers.

#### Development Progress

Key development milestones included:
- Implementing the login and registration system with role-based access
- Creating the inventory management interface
- Building the admin panel for managers
- Adding the sales recording system
- Securing all sensitive user data

#### Testing and Quality Assurance

A comprehensive testing strategy was implemented to ensure the reliability and security of the **Glory Days Inventory Management System**. The following testing types were conducted:

- **Unit Testing**: Core features such as inventory management, user authentication, and data validation were tested in isolation to verify correctness.
- **Integration Testing**: Components including the Python backend, HTML/CSS/JavaScript frontend, and the SQLite database were tested together to ensure seamless interaction across the system.
- **Security Testing**: Password handling and authentication processes were tested for robustness. Hashing using `hashlib` was verified, and common security threats (e.g., SQL injection, brute-force login attempts) were tested and mitigated.
- **Automated End-User Testing**: Selenium was used to simulate real user interactions with the application. Automated test cases were run to mimic typical employee and manager workflows, ensuring the application functioned as expected under real-world scenarios.
- **Final Validation**: All tests confirmed system stability, correct functionality, and a user-friendly interface across use cases.

At the time of release, there were no known issues. The application is considered production-ready, though minor bugs may arise in future use.


#### Bug Fixes and Enhancements

- Fixed form submission bugs in the inventory page
- Improved password validation and error messaging
- Enhanced platform selection dropdown and UI polish

---

### Deployment

The application is deployed locally and is launched by navigating to the `/src` directory and executing `python app.py`. No downtime or major issues were encountered during deployment.

For installation information please read `glory_days_installation_guide` located in the `docs` folder.

---

### Release Notes

#### New Features

- Secure employee and manager login system
- Inventory management tools (add, search, update, delete)
- Sales tracking with dynamic updates to stock
- Admin portal for managing employees and viewing monthly sales

#### Bug Fixes

- Input validation improved on registration and inventory forms
- Corrected issues with updating stock and deleting items

#### Known Issues

No known issues were found during testing, though minor bugs may still be present as this is the initial release. Users are encouraged to report any issues to:

[dtmcloughlin@my.waketech.edu](mailto:dtmcloughlin@my.waketech.edu)  

---

### Conclusion

Version 1.0 of the Glory Days Inventory Management System successfully delivers a complete inventory system application for the Glory Days retail store. Future plans may include expanding database support, enabling cloud hosting, and adding data analytics features for deeper business insights.

