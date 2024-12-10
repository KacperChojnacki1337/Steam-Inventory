#!/usr/bin/env python
# coding: utf-8

# In[2]:


import psycopg2, urllib.request, json, tkinter, time
from sqlalchemy import create_engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import tkinter as tk
from tkinter import ttk

conn = None
cursor = None

def connect_to_db():
    global conn,cursor
    try:
        db_host = "localhost"
        db_port = 5432
        db_name = "steam_inventory"
        db_user = "postgres"
        db_password = "password"
        # Connect to PostgreSQL database
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    except (Exception, psycopg2.Error) as e:
        print("Error connecting to database:", e)

def get_unique_values():
    global conn, cursor
    if not conn:
        connect_to_db()

    try:
        cursor.execute("SELECT item_number || ' ' || item_name FROM inventory GROUP BY item_number, item_name order by item_number;")
        unique_items = [row[0] for row in cursor]
        cursor.execute("SELECT  id || ' ' || channel FROM sales_channels group by id,channel order by id;")
        unique_channels = [row[0] for row in cursor]
        return unique_items, unique_channels
    except (Exception, psycopg2.Error) as e:
        print("Error getting data from table:", e)
        return []

unique_items,unique_channels= get_unique_values()


def remove_from_inventory(item_number):
    try:
        cursor.execute("DELETE FROM inventory WHERE item_number = %s", (item_number,))
        conn.commit()
        success_label.config(text="Item has been removed from inventory.")
    except (Exception, psycopg2.Error) as e:
        error_label.config(text="Error while removing item from inventory: " + str(e))

def add_data_to_db():
    global conn, cursor
    if not conn:
        connect_to_db()
    sales_date = sales_date_entry.get()
    item_number= selected_item.get()
    print(item_number)
    item_number = int(selected_item.get().split(' ')[0])
    print(item_number)
    channel_id = int(selected_channel.get().split(' ')[0])
    selling_price_real_pln = selling_price_real_pln_entry.get()
    selling_price_steam_pln = selling_price_steam_pln_entry.get()
    # Checking if fields are not empty 
    if not sales_date or not item_number or not channel_id or not selling_price_real_pln or not selling_price_steam_pln:
        error_label.config(text="All fields have to be filled")
        return

    # Connecting with database
    try:
        with conn:
            # Insert into sales_data
            print(item_number)
            sql = "INSERT INTO sales_data (sales_date, item_number, channel_id, selling_price_real_pln, selling_price_steam_pln) VALUES (%s, %s, %s, %s, %s)"
            val = (sales_date, item_number, channel_id, selling_price_real_pln, selling_price_steam_pln)
            cursor.execute(sql, val)

            # Delete from inventory
            print(item_number)
            cursor.execute("DELETE FROM inventory WHERE item_number = %s", (item_number,))
            cursor.execute("REFRESH MATERIALIZED VIEW vw_inventory_sales")
        success_label.config(text="Successfully added and removed from inventory.")
    except psycopg2.Error as e:
        error_label.config(text="Error: " + str(e))
    finally:
        if conn:
            cursor.close()
            conn.close()   
        
        
# main
root = tk.Tk()
root.title("Sales")

# labels and text
sales_date_label = tk.Label(root, text="Sales Date:")
sales_date_entry = tk.Entry(root)

item_number_label = tk.Label(root, text="Item Number:")
item_number_entry = tk.Entry(root)

channel_id_label = tk.Label(root, text="Channel Name:")
channel_id_entry = tk.Entry(root)

selling_price_real_pln_label = tk.Label(root, text="Sell Price (PLN):")
selling_price_real_pln_entry = tk.Entry(root)

selling_price_steam_pln_label = tk.Label(root, text="Sell Price (PLN, Steam):")
selling_price_steam_pln_entry = tk.Entry(root)

# add button
add_button = tk.Button(root, text="Add", command=add_data_to_db)

# labels 
error_label = tk.Label(root, text="", fg="red")
success_label = tk.Label(root, text="", fg="green")




# String variable to hold the selected values
selected_channel = tk.StringVar()
selected_channel.set(unique_channels[0])  # Set default value

selected_item = tk.StringVar()
selected_item.set(unique_items[0])



# Create the dropdown menu with unique channels
channel_dropdown = tk.OptionMenu(root, selected_channel, *unique_channels)
item_number_dropdown = tk.OptionMenu(root,selected_item,*unique_items)

# elements to window

# Labels and positioning
sales_date_label.grid(row=1, column=0)
sales_date_entry.grid(row=1, column=1)

item_number_label.grid(row=2, column=0)
item_number_dropdown = ttk.Combobox(root, textvariable=selected_item, values=unique_items)
item_number_dropdown.grid(row=2, column=1)

# Place the dropdown menu before the entry field
channel_id_label.grid(row=3, column=0)
channel_dropdown = ttk.Combobox(root, textvariable=selected_channel, values=unique_channels)
channel_dropdown.grid(row=3, column=1)  

selling_price_real_pln_label.grid(row=4, column=0)
selling_price_real_pln_entry.grid(row=4, column=1)

selling_price_steam_pln_label.grid(row=5, column=0)
selling_price_steam_pln_entry.grid(row=5, column=1)


add_button.grid(row=6, column=0, columnspan=2)
error_label.grid(row=7, column=0, columnspan=2)
success_label.grid(row=8, column=0, columnspan=2)


#run sql connection
connect_to_db()
# run main tkinter
root.mainloop()



# In[ ]:





# In[ ]:




