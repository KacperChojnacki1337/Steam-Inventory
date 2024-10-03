# Steam Inventory Tracker

Steam Inventory Tracker is a Python application that allows you to manage your Steam inventory. The application uses the Tkinter library for the graphical user interface and PostgreSQL for the database.

## Features

- **View Inventory**: Browse all items in your inventory.
- **Add Items**: Add new items to the database.
- **Edit Items**: Edit existing items.
- **Remove Items**: Delete items from the database.
- **Update Prices**: Update item prices based on Steam market data.

## Requirements

- Python 3.x
- Libraries: `psycopg2`, `sqlalchemy`, `tkinter`
- PostgreSQL database

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/KacperChojnacki1337/Steam-Inventory.git
    cd steam-inventory-tracker
    ```

2. Install the required libraries:
    ```bash
    pip install psycopg2 sqlalchemy
    ```

3. Set up the PostgreSQL database:
    - Create a new database named `inventory`.
    - Create the `inventory` table with the appropriate columns.

4. Run the application:
    ```bash
    python steam_inventory_tracker.py
    ```

## Usage

1. Launch the application to open the main user interface window.
2. Use the buttons and text fields to add, edit, delete, and view items in your inventory.
3. Click the "Update All" button to update item prices based on Steam market data.



## Author

- Kacper Chojnacki - https://github.com/KacperChojnacki1337

## License

This project is licensed under the MIT License - see the LICENSE file for details.
