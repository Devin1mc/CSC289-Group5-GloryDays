# **CSC289 Programming Capstone**

# **Project Plan**

**Project Name:** Glory Days Management System

**Team Number:** Group 5

**Team Project Manager / Scrum Master:** Devin McLoughlin

# **Team Member Details**

| Name | Email | Role |
| --- | --- | --- |
| Devin McLoughlin | [dtmcloughlin@my.waketech.edu](mailto:dtmcloughlin@my.waketech.edu) | Project Lead
| Ryan McWhirt | [rdmcwhirt@my.waketech.edu](mailto:rdmcwhirt@my.waketech.edu) | Developer |
| Terry Wiggins | [Ttle6@my.waketech.edu](mailto:Ttle6@my.waketech.edu) | Developer |
| Anthony De Casas Mata | [Adecasasmata@my.waketech.edu](mailto:Adecasasmata@my.waketech.edu) | Developer |
| Thomas Coates | [tacoates@my.waketech.edu](mailto:tacoates@my.waketech.edu) | Developer |

# **Project Goal**

The overall goal of this project is to create a standalone inventory management system with a user-friendly interface specifically designed for small retail businesses, “Glory Days”. The system should be able to take in employee (user) input to add or take away items within the current inventory stock. Price comparisons should be made from the data of inventory items sold and this can help employees price new items.

# **Project Objectives**

Efficient Inventory Tracking: Develop a real-time inventory tracking feature by Sprint 2, ensuring 100% accurate updates for sales and purchases.

Price Trend Analysis: Implement a web scraping feature by Sprint 3 to retrieve pricing trends for 90% of retro gaming items.

Adding New Inventory Items: Enable tracking all (100%) new inventory items, including prices, by Sprint 3.

User-Friendly Interface: Design a GUI by Sprint 2 with 90% usability test approval, ensuring intuitive inventory management.

# **Project Scope**

Included:

- The software will store inventory data in a database using SQLite for simplicity and reliability.
- The software will function as a standalone application, requiring no additional external systems.
- The user interface will be intuitive and developed using a modern framework (e.g., HTML/CSS/JavaScript).
- The application logic will primarily use Python for backend functionality and JavaScript for interactive front-end features.
- The software will be designed to run on standard retail business computers without requiring specialized hardware.

Excluded:

- The software will not include features for integration or collaboration with external distributors or warehouse systems.
- The software will not include mobile or tablet compatibility; it will be designed specifically for desktop use.
- The software will not support multi-location inventory management for businesses with multiple stores.

# **Project Assumptions**

- Availability of Resources: all team members will be available throughout the duration of the project without absence and all team members will have access to all resources 24/7
- Knowledge of Team Apps: all team members understand how to use the various platforms required for the project (GitHub, Trello, Microsoft Teams)
- Software Requirements: the team will have access to all required software, whether that be a code editor (IDE), live or local server, etc.
- User Behavior: Users of our application will utilize the software as intended and adapt to any necessary changes in the UI or functionality.
- Regulatory Compliance: The software will comply with all relevant regulations and legal requirements throughout its lifecycle
- Availability and Stability of Third-Party APIs: Any/all third-party APIs required for the App will remain available, stable, and perform as expected.

# **Project Constraints**

- Budget Constraints: The project must be developed within a limited budget, restricting the use of expensive third-party tools or premium software solutions, and the team must rely on free or open-source resources (e.g., SQLite, Python libraries, and development frameworks).
- Time Constraints: The project timeline is tied to the semester schedule, requiring strict adherence to deadlines for Sprints 2 and 3, leaving little room for delays in development, testing, and debugging.
- Technical Constraints: The system must run on standard retail business computers with limited hardware capabilities, and it must use SQLite for data storage while adhering to the team’s current technical expertise in Python, HTML, CSS, or JavaScript.
- Regulatory and Compliance Constraints: The software must comply with all applicable legal and data privacy regulations, which may impose restrictions on how user and inventory data are stored, processed, and accessed.
- Testing and Usability Constraints: The GUI must achieve a 90% usability approval rate in simulated retail testing environments, but limited resources may prevent testing all real-world use cases.

# **Project Resources Required**

Flask – Facilitate creating and managing the website used to store business inventory. Can also incorporate Bootstrap if needed. Simplicity and ease of use will be helpful to those with web programming difficulty.

Trello – Will be used to track each member's task assignments and will reduce confusion on how each task will be implemented. Each member will be assigned tasks depending on the sprint or any deviation to the plan and will be required to complete it within a given time frame.

Microsoft Teams – Will be the team's main method of contact and be used to communicate changes, check on other team members, and handle potential problems on the project

GitHub – Will be used to manage changes in programs, revise work, document version control, and check program progress. A main branch will be used for the project and team members will create their own branches which will then be pushed depending on team feedback.

SQL – Will be used to store business inventory and will be updated daily depending on other business trends/inventory prices. It can be used to calculate our own prices vs other business prices to raise or minimize business profit.

Playwright - Will be used to get other business information on their prices and will highlight important information like stock count, price, and type. Web scraped data will be in Json format and be used on SQL.

**Team Collaboration and Communication**

- **GitHub – Version Control:** GitHub will be utilized as the primary version control system for the project. Each team member will contribute to a shared repository, following best practices for branching, committing, and merging code. Pull requests and issue tracking will be used to manage code reviews and bug tracking. The repository will be organized with clear documentation to ensure seamless collaboration.
- **Microsoft Teams – Daily Communication:** Microsoft Teams will serve as the main platform for daily communication and coordination among team members. It will be used for instant messaging, voice/video calls, and quick discussions related to project progress. Weekly meetings will be scheduled to discuss challenges, assign tasks, and ensure alignment on development goals. Important project files and documentation will also be stored in dedicated Teams channels for easy reference.
- **Trello – Task Management:** A Trello board will be used to organize and track tasks throughout the project lifecycle. The board will be structured using columns such as “To-Do,” “In Progress,” “Review,” and “Completed” to visually represent the workflow. Each task will include detailed descriptions, deadlines, and assigned team members to ensure accountability. The board will be regularly updated to reflect current progress and upcoming milestones.

**Project Documentation**

- Microsoft Word - the primary tool for drafting, formatting, and finalizing project documents. It allows for collaborative editing through track changes and comments, making it easier for team members to review and provide feedback. Additionally, documents will be stored in **OneDrive or SharePoint** to ensure cloud-based access and version control.
- GitHub - to maintain project-related documentation alongside the code repository. The **GitHub Wiki** will serve as a structured knowledge base containing essential details such as setup instructions, API documentation, and troubleshooting guides. Additionally, **ReadMe files** will provide an overview and usage instructions to ensure clarity for developers and users.
- Trello – This will help set priorities, monitor progress, and assign tasks, providing a visual representation of the project’s status. This ensures that deadlines are met and that every team member remains accountable for their assigned responsibilities.

**Project Management Plan and Methodologies**

The project will follow the Agile methodology using Scrum, structured into two-week sprints with clear deliverables.

Sprint Structure:

- Sprint Planning: Define backlog items, assign tasks, and estimate time.
- Daily Standups: Brief updates on progress and blockers via Microsoft Teams.
- Sprint Reviews & Retrospectives: Demo completed work and identify improvements.

Tools & Collaboration:

- Trello – Task management and backlog tracking
- GitHub – Version control and issue tracking
- Microsoft Teams – Communication and document sharing

Testing & Deployment:

- Unit and integration testing ensure quality.
- Final sprint focuses on bug fixes, optimizations, and deployment.