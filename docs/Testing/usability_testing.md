# Usability Testing Session: End-User Perspective

---

## Task 1: Logging In

**Scenario:**  
I open the application URL and arrive at the login page. The page displays the “Glory Days” logo and a clean, simple login form.

**Actions:**  
- Enter my Employee ID and password.  
- Notice that the form fields are clearly labeled, with straightforward styling from **login.css**.

**Observations:**  
- The design is minimalistic, which helps me focus on entering credentials.  
- The contrast between the form text and the background is acceptable, although some users might prefer even higher contrast for better accessibility.

---

## Task 2: Registration

**Scenario:**  
I click on the “Register” button to create a new account.

**Actions:**  
- I am directed to the registration page (using **register.html**).  
- I fill in my first name, last name, Employee ID, and choose a password.  
- I select my role from a dropdown menu.

**Observations:**  
- The registration page layout is similar to the login page, ensuring a consistent user experience.  
- All fields are clearly laid out, making the registration process feel intuitive.

---

## Task 3: Navigating the Inventory

**Scenario:**  
After logging in, I am redirected to the inventory page (rendered via **inventory.html** with styling from **inventory.css**).

**Actions:**  
- My name is displayed at the top, confirming successful login.  
- I see a list of inventory items showing SKU, name, stock, price, and condition.  
- I use the search bar to filter items by name or SKU and click the sort buttons (e.g., “Sort by Name”).

**Observations:**  
- The inventory list is well-organized with clear labels.  
- Search and sorting functions are responsive and provide immediate visual feedback.  
- The dark background with contrasting text from **inventory.css** gives the page a modern look.

---

## Task 4: Adding and Editing Inventory Items

**Scenario:**  
I decide to add a new item to the inventory.

**Actions:**  
- I click the “Add Item” button, which opens a centered dialog.  
- The dialog (styled in **inventory.css**) contains fields for item code, name, quantity, price, and condition.  
- I update an existing item by clicking its edit button, and the pre-populated dialog makes it easy to modify the details.

**Observations:**  
- The dialog is clear and easy to use.  
- Interactive elements such as buttons and input fields provide immediate feedback, making the task feel smooth and error-free.

---

## Task 5: Selling an Item

**Scenario:**  
I want to process a sale for one of the inventory items.

**Actions:**  
- I click the “Sell” button on a specific item.  
- The system processes the sale (using the backend logic in **app.py**) and updates the item’s stock.  
- A confirmation message informs me that the sale was successful.

**Observations:**  
- The sale process is quick and clearly indicated by the updated stock count.  
- Real-time feedback reassures me that my action was registered correctly.

---

## Task 6: Reviewing Sales Data and Accessing the Admin Panel

**Scenario:**  
I navigate to the Sales page and, if logged in as an admin, explore the Admin Control Panel.

**Actions:**  
- On the Sales page (built with **sales.html**), I see a table listing recent sales, including item code, condition, quantity, sale price, and sale date.  
- I then access the Admin Panel (via **admin.html** styled by **admin.css**) where I view user lists and inventory management options.

**Observations:**  
- Both pages are organized and easy to interpret.  
- The table layouts and navigation links (such as “Back to Inventory” and “Logout”) are clear and function as expected.  
- The admin interface neatly separates inventory and user management functions, supporting a clear workflow.

---

## Overall End-User Feedback

**Intuitiveness:**  
- The application flows logically from logging in and registering to managing inventory and processing sales.  
- Each task is clear and doesn’t require additional guidance.

**Design Consistency:**  
- Consistent styling across all pages (via dedicated CSS files) enhances the user experience by maintaining a cohesive look and feel.

**Interactive Feedback:**  
- Actions like searching, sorting, adding, editing, and selling items provide immediate responses, which is crucial for user confidence.

**Potential Improvements:**  
- **Accessibility:** Although the contrast is generally sufficient, some users might benefit from slightly higher contrast in the login and form elements.  
- **Real-Time Updates:** Enhancing live update functionality on the inventory page (for search and sort operations) could further improve user satisfaction.  
- **Hover & Focus States:** Adding more noticeable hover or focus effects on interactive elements can help users identify clickable items more clearly.

---

## Conclusion

As an end user, I found the inventory management application to be generally intuitive, user-friendly, and visually consistent. With minor tweaks to improve accessibility and interactive feedback, the system could provide an even more seamless experience. This testing session confirms that the design, functionality, and overall user flow are well-aligned with usability best practices.
