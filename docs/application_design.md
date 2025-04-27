# Glory Days Inventory System

## System Overview

The **Glory Days Inventory System** is designed for managing inventory and employee information. It includes registration, login, inventory management, and admin roles with access to sales data.

## Mermaid Diagram

```mermaid
graph TD
    A[User Registration] --> B[Store Credentials in login_database.db]
    A --> C[Hash Password using hashlib]
    C --> B

    D[Employee Login] --> E[Check Credentials in login_database.db]
    E --> F[If Valid, Login Successful]
    E --> G[If Invalid, Retry Login]

    F --> H[Inventory Page]
    H --> I[Add Item to Inventory]
    H --> J[Update Inventory Item]
    H --> K[Remove Item from Inventory]
    H --> L[View Inventory Items]
    L --> M[Database_inventory.db]
    
    H --> N[Admin Button - Access Admin Page for Managers]
    N --> O[Remove Employee from login_database.db]
    N --> P[Go to Inventory Page]
    N --> Q[Go to Sales Page]

    Q --> R[View Sales Data from sales table in inventory.db]
    Q --> S[Save Sales Data as PDF]

    style A fill:#f9f,stroke:#333,stroke-width:4px, color:#000
    style B fill:#ccf,stroke:#333,stroke-width:2px, color:#000
    style C fill:#dfd,stroke:#333,stroke-width:2px, color:#000
    style D fill:#ffb,stroke:#333,stroke-width:2px, color:#000
    style E fill:#ffb,stroke:#333,stroke-width:2px, color:#000
    style F fill:#dfd,stroke:#333,stroke-width:2px, color:#000
    style G fill:#fbb,stroke:#333,stroke-width:2px, color:#000
    style H fill:#ccf,stroke:#333,stroke-width:2px, color:#000
    style I fill:#cfc,stroke:#333,stroke-width:2px, color:#000
    style J fill:#cfc,stroke:#333,stroke-width:2px, color:#000
    style K fill:#cfc,stroke:#333,stroke-width:2px, color:#000
    style L fill:#cfc,stroke:#333,stroke-width:2px, color:#000
    style M fill:#ccf,stroke:#333,stroke-width:2px, color:#000
    style N fill:#f9f,stroke:#333,stroke-width:2px, color:#000
    style O fill:#f9f,stroke:#333,stroke-width:2px, color:#000
    style P fill:#ccf,stroke:#333,stroke-width:2px, color:#000
    style Q fill:#ffb,stroke:#333,stroke-width:2px, color:#000
    style R fill:#cfc,stroke:#333,stroke-width:2px, color:#000
    style S fill:#cfc,stroke:#333,stroke-width:2px, color:#000
