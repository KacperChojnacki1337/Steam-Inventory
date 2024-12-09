import Currency_Webscrapping
import pandas as pd
import datetime


df= Currency_Webscrapping.get_nbp_data("USD", "2024-01-01", Currency_Webscrapping.endDay)
last_row = df.iloc[-1].copy() 
last_row['date'] += datetime.timedelta(days=1)
df = pd.concat([df, last_row.to_frame().T], ignore_index=True) 
df
Currency_Webscrapping.insert_data_to_postgresql(df)

import psycopg2, urllib.request, json, tkinter, time
from sqlalchemy import create_engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def column_maker(value, column_length):
    if type(value) != str:
        num_add_char = column_length - int(len(str(value)))
        add_char = num_add_char * " "
        return "".join([str(value), add_char])
    else:
        num_add_char = column_length - int(len(value))
        add_char = num_add_char * " "
        return "".join([value, add_char])


class InventoryWindow(tkinter.Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Inventory Viewer")
        self.configure(background='grey')
        self.geometry('700x500')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        tkinter.Label(self, text="Inventory", font=('Segoe UI Bold', 9), background='grey', fg='white') \
            .grid(row=0, column=0, sticky='s', columnspan=2)
        self.inventory_listbox = tkinter.Listbox(self)
        self.inventory_listbox.grid(row=1, column=0, sticky='nsew', columnspan=2)

        inventory_scrollbar_y = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        inventory_scrollbar_x = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL)
        inventory_scrollbar_y.grid(row=1, column=0, sticky='nse', columnspan=2)
        inventory_scrollbar_x.grid(row=1, column=0, sticky='sew', columnspan=2)

        self.inventory_listbox.config(yscrollcommand=inventory_scrollbar_y.set)
        self.inventory_listbox.config(xscrollcommand=inventory_scrollbar_x.set)
        inventory_scrollbar_y.config(command=self.inventory_listbox.yview)
        inventory_scrollbar_x.config(command=self.inventory_listbox.xview)
        inventory_stats = tkinter.Button(self, text="Show Inventory Statistics", command=self.inventory_statistics)
        inventory_stats.grid(row=2, column=0, sticky='w', padx=10)
        self.inventory_stats_result = tkinter.Label(self, background='grey', fg='white')
        self.inventory_stats_result.grid(row=2, column=1, sticky='w', padx=8, pady=5)

        self.inventory_listbox.config(font="TkFixedFont")

    def inventory_statistics(self):
        cursor.execute("SELECT total_value FROM inventory")
        value_items = cursor.fetchall()
        total_inventory_value = 0
        for price in value_items:
            total_inventory_value += price[0]

        cursor.execute("SELECT total_cost FROM inventory")
        cost_items = cursor.fetchall()
        total_inventory_cost = 0
        for cost in cost_items:
            total_inventory_cost += cost[0]
  
        self.inventory_stats_result.config(
            text=f"Total Inventory Value: {total_inventory_value}\n Total Inventory Cost: {total_inventory_cost}")

    def update_inventory_display(self):
        global conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        item_tuple = cursor.fetchall()
        number_length = 10   # int
        buy_date_length = 10     # str
        item_length = 50    # str
        cost_per_item_length = 17    # float
        number_of_items_length = 19  # int
        current_price_length = 17    # float
        total_cost_length = 14       # float
        total_value_length = 15      # float
        total_return_percent_length = 24    # float
        total_return_dollar_length = 20     # float
        item_link_length = 100
        purchase_info_length = 20 # int
        real_cost_per_item_length = 17 # float
        real_total_cost_length = 17 #float
        # number, date, item, cost_per_item, number_of_items, current_price, total_cost, total_value, total_return_percent, total_return_dollar, item_link, purchase_info, real cost per item, real total cost
 
        printable_list = []
        for number, buy_date, item, cost_per_item, number_of_items, current_price, total_cost, total_value,\
            total_return_percent, total_return_dollar, item_link, purchase_info, real_cost_per_item,real_total_cost in item_tuple:
            printable_list.append(column_maker(number, number_length))
            printable_list.append(column_maker(buy_date, buy_date_length))
            printable_list.append(column_maker(item, item_length))
            printable_list.append(column_maker(cost_per_item, cost_per_item_length))
            printable_list.append(column_maker(number_of_items, number_of_items_length))
            printable_list.append(column_maker(current_price, current_price_length))
            printable_list.append(column_maker(total_cost, total_cost_length))
            printable_list.append(column_maker(total_value, total_value_length))
            printable_list.append(column_maker(total_return_percent, total_return_percent_length))
            printable_list.append(column_maker(total_return_dollar, total_return_dollar_length))
            printable_list.append(column_maker(item_link, item_link_length))
            printable_list.append(column_maker(purchase_info,purchase_info_length))
            printable_list.append(column_maker(real_cost_per_item,real_cost_per_item_length))
            printable_list.append(column_maker(real_total_cost,real_total_cost_length))

        group_list = [tuple(printable_list[n: n+14]) for n in range(0, len(printable_list), 14)]
        item_list = [''.join(x) for x in group_list]

        column_headers = ['Item #', 'Buy Date', 'Item Name', 'Cost Per Item', 'Number of Items', 'Current Price',
                          'Total Cost', 'Total Value', 'Total Return Percent', 'Total Return Value', 'Item Link', 'Purchase Info','Real Cost Per Item','Real Total Cost']

        column_headers_centered = []
        index = 0
        column_lengths = [number_length, buy_date_length, item_length, cost_per_item_length, number_of_items_length,
                          current_price_length, total_cost_length, total_value_length, total_return_percent_length,
                          total_return_dollar_length, item_link_length,purchase_info_length,real_cost_per_item_length,real_total_cost_length]

        for column in column_headers:
            y = column.center(column_lengths[index])
            column_headers_centered.append(y)
            index += 1

        group_list2 = [tuple(column_headers_centered[n: n+14]) for n in range(0, len(column_headers_centered), 14)]
        column_headers_string = [''.join(x) for x in group_list2]

        new_list = column_headers_string + item_list

        for item in new_list:
            self.inventory_listbox.insert(tkinter.END, item)


class SteamInventory(tkinter.Tk):

    def __init__(self, conn):
        super().__init__()
        self.item_number = None
        self.item_link = None
        self.buy_date = None
        self.cost_per_item = None
        self.number_of_items = None
        self.current_price = None
        self.item_name = None
        self.total_value = None
        self.total_cost = None
        self.total_return_percent = None
        self.total_return_dollar = None
        self.purchase_info = None
        self.real_cost_per_item = None
        self.real_total_cost = None
        self.cursor = conn.cursor()

        # ==== GUI ====
        self.title("Steam Inventory Tracker")
        self.configure(background='grey')
        self.geometry('600x600')

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)
        self.rowconfigure(13, weight=1)
        self.rowconfigure(14, weight=1)
        self.rowconfigure(15, weight=1)
        self.rowconfigure(16, weight=1)
        self.rowconfigure(17, weight=1)
        self.rowconfigure(18, weight=1)

        # ==== SELECT ITEM: (if edit or remove) ====
        tkinter.Label(self, text="Item List", font=('Segoe UI Bold', 9), fg='white', background='grey') \
            .grid(row=0, column=0, sticky='s', columnspan=2, pady=2, padx=5)

       
        #change length of listbox                     
        self.select_item_listbox = tkinter.Listbox(self)
        self.select_item_listbox.grid(row=1, column=0, rowspan=14, sticky='nsew', columnspan=2, padx=5)

        self.select_item_scrollbox = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        self.select_item_scrollbox.grid(row=1, column=0, rowspan=14, columnspan=2, sticky='nse')

        self.select_item_listbox.config(yscrollcommand=self.select_item_scrollbox.set)
        self.select_item_scrollbox.config(command=self.select_item_listbox.yview)
                   
        # ==== EDIT ITEM ====
        tkinter.Label(self, text='Add/Edit Item', font=('Segoe UI Bold', 9), fg='white', background='grey')\
            .grid(row=0, column=3, columnspan=2, pady=2, padx=5)

        tkinter.Label(self, text='Item Number (KEY):', fg='white', background='grey').grid(row=1, column=3, sticky='w')
        tkinter.Label(self, text='Item name (Optional):', fg='white', background='grey')\
            .grid(row=2, column=3, sticky='w')
        tkinter.Label(self, text='Buy Date:', fg='white', background='grey').grid(row=3, column=3, sticky='w')
        tkinter.Label(self, text='Cost per item:', fg='white', background='grey').grid(row=4, column=3, sticky='w')
        tkinter.Label(self, text='Number of items:', fg='white', background='grey').grid(row=5, column=3, sticky='w')
        tkinter.Label(self, text='Current price:', fg='white', background='grey').grid(row=6, column=3, sticky='w')
        tkinter.Label(self, text='Steam Market Link:', fg='white', background='grey').grid(row=7, column=3, sticky='w')
        tkinter.Label(self, text='Purchase Info:', fg='white', background='grey').grid(row=8, column=3, sticky='w')
        tkinter.Label(self, text='Real Cost Per Item:', fg='white', background='grey').grid(row=9, column=3, sticky='w')
       
        self.item_number_input = tkinter.StringVar()
        self.item_name_input = tkinter.StringVar()
        self.buy_date_input = tkinter.StringVar()
        self.cost_per_item_input = tkinter.StringVar()
        self.number_of_items_input = tkinter.StringVar()
        self.current_price_input = tkinter.StringVar()
        self.steam_market_link_input = tkinter.StringVar()
        self.purchase_info_input = tkinter.StringVar()
        self.real_cost_per_item_input = tkinter.StringVar()
        ####
        item_number_entry = tkinter.Entry(self, textvariable=self.item_number_input)
        item_name_entry = tkinter.Entry(self, textvariable=self.item_name_input)
        buy_date_entry = tkinter.Entry(self, textvariable=self.buy_date_input)
        cost_per_item_entry = tkinter.Entry(self, textvariable=self.cost_per_item_input)
        number_of_item_entry = tkinter.Entry(self, textvariable=self.number_of_items_input)
        current_price_entry = tkinter.Entry(self, textvariable=self.current_price_input)
        steam_market_link_entry = tkinter.Entry(self, textvariable=self.steam_market_link_input)
        purchase_info_entry = tkinter.Entry(self, textvariable=self.purchase_info_input)
        real_cost_per_item_entry = tkinter.Entry(self, textvariable=self.real_cost_per_item_input)

        item_number_entry.grid(row=1, column=4, sticky='nsew', padx=5, pady=2)
        item_name_entry.grid(row=2, column=4, sticky='nsew', padx=5, pady=2)
        buy_date_entry.grid(row=3, column=4, sticky='nsew', padx=5, pady=2)
        cost_per_item_entry.grid(row=4, column=4, sticky='nsew', padx=5, pady=2)
        number_of_item_entry.grid(row=5, column=4, sticky='nsew', padx=5, pady=2)
        current_price_entry.grid(row=6, column=4, sticky='nsew', padx=5, pady=2)
        steam_market_link_entry.grid(row=7, column=4, sticky='nsew', padx=5, pady=2)
        purchase_info_entry.grid(row=8, column=4, sticky='nsew', padx=5, pady=2)
        real_cost_per_item_entry.grid(row=9, column=4, sticky='nsew', padx=5, pady=2)

        add_button = tkinter.Button(self, text='Add', command=self.add_item)
        add_button.grid(row=10, column=3, sticky='new', padx=14, pady=8)

        self.edit_button = tkinter.Button(self, text='Edit', command=self.edit_item)
        self.edit_button.grid(row=10, column=4, sticky='new', padx=14, pady=8)

        self.edit_result = tkinter.Label(self, background='grey')
        self.edit_result.grid(row=11, column=3, sticky='n', columnspan=2)
               ###########
        # ==== REMOVE ITEM ====
        tkinter.Label(self, text="Remove Item", font=('Segoe UI Bold', 9), fg='white', background='grey')\
            .grid(row=12, column=3, columnspan=2, padx=5, pady=2)
        tkinter.Label(self, text='Item Number:', fg='white', background='grey')\
            .grid(row=13, column=3, padx=5, pady=2, sticky='w')

        self.item_number_to_remove = tkinter.IntVar()
        remove_item_entry = tkinter.Entry(self, textvariable=self.item_number_to_remove)
        remove_item_entry.grid(row=13, column=4, sticky='nsew', padx=5, pady=2)

        remove_item_button = tkinter.Button(self, text='Enter', command=self.remove_item)
        remove_item_button.grid(row=14, column=3, columnspan=2, sticky='new', padx=80, pady=8)
    
        self.remove_item_result = tkinter.Label(self, background='grey')
        self.remove_item_result.grid(row=15, column=3, columnspan=2)
      
        # ==== CURRENT PRICE UPDATE ====
        tkinter.Label(self, text="Current Price Update", font=('Segoe UI Bold', 9), fg='white', background='grey')\
            .grid(row=16, column=0, columnspan=2)

        update_prices = tkinter.Button(self, text="Update All", command=self.update_price)
        update_prices.grid(row=17, column=0, columnspan=2, sticky='nsew', padx=80, pady=8)

        self.update_price_result = tkinter.Label(self, fg='white', background='grey')
        self.update_price_result.grid(row=18, column=0, columnspan=2, sticky='n')

        # ==== BLANK COLUMNS AND ROWS ====
        tkinter.Label(self, padx=8, background='grey').grid(row=16, column=3)
        tkinter.Label(self, padx=8, background='grey').grid(row=11, column=3)

        show_inventory = tkinter.Button(self, text='Show Inventory', command=self.open_inventory)
        show_inventory.grid(row=18, column=3, columnspan=2, sticky='nsew', padx=80, pady=8)

    def open_inventory(self):
        inventory_window = InventoryWindow(self)
        inventory_window.update_inventory_display()

    def get_input(self):

        self.item_number = self.item_number_input.get()

        if len(self.item_name_input.get()) == 0:
            self.item_name = None
        else:
            self.item_name = self.item_name_input.get()

        if len(self.buy_date_input.get()) == 0:
            self.buy_date = None
        else:
            self.buy_date = self.buy_date_input.get()

        if len(self.cost_per_item_input.get()) == 0:
            self.cost_per_item = None
        else:
            self.cost_per_item = float(self.cost_per_item_input.get())

        if len(self.number_of_items_input.get()) == 0:
            self.number_of_items = None
        else:
            self.number_of_items = int(self.number_of_items_input.get())

        if len(self.current_price_input.get()) == 0:
            self.current_price = None
        else:
            self.current_price = float(self.current_price_input.get())

        if len(self.steam_market_link_input.get()) == 0:
            self.item_link = None
        else:
            self.item_link = self.steam_market_link_input.get()
                                  
        if len(self.purchase_info_input.get()) == 0:
            self.purchase_info = None
        else:
            self.purchase_info = self.purchase_info_input.get()
        
        try:
            self.real_cost_per_item = float(self.real_cost_per_item_input.get())
        except ValueError:
            self.real_cost_per_item = 0
            
            
                                  

    def add_item(self):
        self.get_input()
        self.cursor.execute("""SELECT item_number FROM inventory WHERE (item_number = %s)""",
                                  (self.item_number,))
        row = self.cursor.fetchone()
        if row:
            self.edit_result.config(text="Item already exists, please select another action", fg='#fda1a1')
            self.edit_result.after(3000, self.reset_result_text)
        else:
            try:
                if self.item_name is None:
                    item_name = self.item_link[47:]
                    self.item_name = item_name.replace("%20", " ").replace("%7C", "|")\
                        .replace("%28", "(").replace("%29", ")").replace("%26", "&")
                self.total_cost = round(self.cost_per_item * self.number_of_items, 2)
                self.total_value = round(self.current_price * self.number_of_items, 2)
                self.real_total_cost = round(self.real_cost_per_item * self.number_of_items,2)
                try:
                    self.total_return_percent = round(((self.current_price - self.cost_per_item) / self.cost_per_item) * 100, 2)
                except ZeroDivisionError:
                    self.total_return_percent = 0
                    
                    #########
                self.total_return_dollar = round(self.total_value - self.total_cost, 2)
                add_sql = "INSERT INTO inventory VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
                self.cursor.execute(add_sql, (self.item_number, self.buy_date, self.item_name, self.cost_per_item,
                                              self.number_of_items, self.current_price, self.total_cost,
                                              self.total_value, self.total_return_percent, self.total_return_dollar,
                                              self.item_link,self.purchase_info,self.real_cost_per_item,self.real_total_cost))
                self.cursor.connection.commit()
                self.edit_result.config(text="Item added", fg='#5bfba3')
                self.edit_result.after(3000, self.reset_result_text)
            except TypeError:
                self.edit_result.config(text="Please enter the required fields to add the item", fg='#fda1a1')
                self.edit_result.after(3000, self.reset_result_text)

        self.item_list_update()
   
    def reset_result_text(self):
        self.edit_result.destroy()
        self.edit_result = tkinter.Label(self, background='grey')
        self.edit_result.grid(row=9, column=3, sticky='n', columnspan=2)

        self.remove_item_result.destroy()
        self.remove_item_result = tkinter.Label(self, background='grey')
        self.remove_item_result.grid(row=14, column=3, columnspan=2)

        self.update_price_result.destroy()
        self.update_price_result = tkinter.Label(self, background='grey')
        self.update_price_result.grid(row=18, column=0, columnspan=2, sticky='n')

    def edit_item(self):
        self.get_input()
        self.cursor.execute("SELECT item_number FROM inventory WHERE (item_number = %s)",
                                  (self.item_number,))
        row = self.cursor.fetchone()

        if row:
            self.cursor.execute("UPDATE inventory SET "
                                "buy_date = COALESCE(%s, buy_date), "
                                "cost_per_item = COALESCE(%s, cost_per_item), "
                                "current_price = COALESCE(%s, current_price), "
                                "number_of_items = COALESCE(%s, number_of_items), "
                                "item_name = COALESCE(%s, item_name), "
                                "item_link = COALESCE(%s, item_link), "
                                "purchase_info = COALESCE(%s, purchase_info), "
                                "real_cost_per_item = COALESCE(%s, real_cost_per_item) "
                                "WHERE item_number = %s", (self.buy_date, self.cost_per_item, self.current_price,
                                                          self.number_of_items, self.item_name, self.item_link,self.purchase_info,self.real_cost_per_item,
                                                          self.item_number))
                                       
            self.cursor.connection.commit()
            self.update_calculations(self.item_number)
            self.edit_result.config(text="Item Updated", fg='#5bfba3')
            self.edit_result.after(3000, self.reset_result_text)
            self.item_list_update()
        else:
            self.edit_result.config(text="Item does not exist", fg='#fda1a1')
            self.edit_result.after(3000, self.reset_result_text)

    def update_calculations(self,item_number):
        self.cursor.execute("SELECT cost_per_item FROM inventory WHERE item_number = %s",
                                            (item_number,))
        cost_per_item =  float(self.cursor.fetchone()[0])
        
        
        self.cursor.execute("SELECT number_of_items FROM inventory WHERE item_number = %s",
                                              (item_number,))
        number_of_items =int(self.cursor.fetchone()[0])
        
        
        self.cursor.execute("SELECT current_price FROM inventory WHERE item_number = %s",
                                            (item_number,))
        current_price = float(self.cursor.fetchone()[0])
        
        
        self.cursor.execute("SELECT real_cost_per_item FROM inventory WHERE item_number = %s",
                                            (item_number,))
        real_cost_per_item =float(self.cursor.fetchone()[0])
        
        self.total_cost = round(cost_per_item * number_of_items, 2)
        self.total_value = round(current_price * number_of_items, 2)
        self.real_total_cost = round(real_cost_per_item * number_of_items,2)
        try:
            total_return_percent = round(((current_price - cost_per_item) / cost_per_item) * 100, 2)
        except ZeroDivisionError:
            total_return_percent = 15
        total_return_dollar = round(self.total_value - self.total_cost, 2)

        self.cursor.execute("UPDATE inventory SET "
                            "total_cost = %s, "
                            "total_value = %s, "
                            "real_total_cost = %s,"
                            "total_return_percent = %s, "
                            "total_return_dollar = %s "
                            "WHERE item_number = %s",
                            (self.total_cost, self.total_value, self.real_total_cost,total_return_percent, total_return_dollar,
                             item_number))
        self.cursor.connection.commit()
        
    def item_list_update(self):
        try:
            if self.cursor is None:
                self.cursor = conn.cursor()  # Zainicjalizuj kursor, jeśli jeszcze tego nie zrobiono
                
            self.cursor.execute("SELECT item_number, item_name FROM inventory")
            item_tuple = self.cursor.fetchall()
            printable_list = [f"{number} : {item}" for number, item in item_tuple]
            self.select_item_listbox.delete(0, tkinter.END)
            for item in printable_list:
                self.select_item_listbox.insert(tkinter.END, item)
    # ... reszta kodu korzystającego z item_tuple
        except Exception as e:
            print(f"Błąd podczas pobierania przedmiotów: {e}")        

    def remove_item(self):
        item_number = self.item_number_to_remove.get()
        self.cursor.execute("SELECT item_number FROM inventory WHERE (item_number = %s)",
                                  (item_number,))
        row = self.cursor.fetchone()

        if row:
            self.cursor.execute("DELETE FROM inventory WHERE item_number = %s", (item_number,))
            self.cursor.connection.commit()
            self.remove_item_result.config(text="Item Removed", fg='#5bfba3')
            self.remove_item_result.after(3000, self.reset_result_text)
        else:
            self.remove_item_result.config(text="Item does not exist", fg='#fda1a1')
            self.remove_item_result.after(3000, self.reset_result_text)

        self.item_list_update()

    def update_price(self):
        self.cursor.execute("SELECT item_link,number_of_items,buy_date FROM inventory")
        row = self.cursor.fetchall()
        for url, number_of_items, buy_date in row:
            market_hash_name = url[47:]
            target_url = "https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=" \
                         + market_hash_name
            num_retries = 3
            item_price = None
            for attempt in range(num_retries):
                try: 
                    url_request = urllib.request.urlopen(target_url)
                    data = json.loads(url_request.read().decode())
                    item_name = market_hash_name.replace('%20', ' ')
                    lowest_price = data.get('lowest_price')
                    if lowest_price is None:
                        raise Exception("Lowest price not found")
                    item_price = str(lowest_price)
                    break
                except Exception as e:
                    print(f"Error fetching lowest price (attempt {attempt + 1}/{num_retries}): {e}")
                    if attempt < num_retries - 1:  # Retry only if not the last attempt
                        time.sleep(15)
            print(url_request)
            print(item_name)
            print(item_price)
            print(data)
            
            if item_price is None or item_price == "" or item_price == "None":
                print("Lowest price not found after retries. Using median price...")
                item_price = str(data.get('median_price'))
            else:
                print("Item price is not None")
                print(item_price)
            item_price = float(item_price.replace('$', ''))
            self.cursor.execute("UPDATE inventory SET current_price = %s WHERE item_link = %s", (item_price, url))
            self.cursor.connection.commit()
            self.cursor.execute("SELECT item_number FROM inventory WHERE item_link = %s AND number_of_items = %s AND buy_date = %s", (url, number_of_items, buy_date))
            item_number = self.cursor.fetchone()[0]
            self.update_calculations(item_number)
            self.update_price_result.config(text=f"Current price for item {item_number} has been updated", fg='#5bfba3')
            self.update()
            time.sleep(4.5)
    
        self.update_price_result.config(text="Current prices updated for all items")
        self.update()

        self.update_price_result.after(3000, self.reset_result_text())

if __name__ == '__main__':
    db_host = "localhost"
    db_port = 5432
    db_name = "steam_inventory"
    db_user = "postgres"
    db_password = "postgres"
        # Connect to PostgreSQL database
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor.execute('SELECT current_database()')
    cursor.fetchall()
    ##############################
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS inventory
               (item_number SERIAL PRIMARY KEY, 
               buy_date DATE NOT NULL,
               item_name TEXT NOT NULL,
               cost_per_item REAL NOT NULL, 
               number_of_items INTEGER NOT NULL, 
               current_price REAL NOT NULL, 
               total_cost REAL NOT NULL, 
               total_value REAL NOT NULL, 
               total_return_percent REAL NOT NULL,
               total_return_dollar REAL, 
               item_link VARCHAR(255) NOT NULL,
               purchase_info INTEGER NOT NULL,
               real_cost_per_item REAL NOT NULL,
               real_total_cost REAL NOT NULL);""")
        print("Tabela utworzona")
    except (psycopg2.Error, Exception) as err:  
        print("Error creating table:", err)
    steam_inventory = SteamInventory(conn)
    steam_inventory.item_list_update()
    steam_inventory.mainloop()
    try:
        # Insert data into inventory_data
        cursor.execute("""
        INSERT INTO inventory_data (
        update_date,
        item_number,
        item_name,
        cost_per_item,
        number_of_items,
        current_price,
        total_cost,
        total_value,
        item_link,
        buy_date,
        purchase_id,
         real_cost_per_item_pln,
         real_total_cost_pln

        )
        SELECT
          to_date(to_char(current_timestamp, 'YYYY-MM-DD'), 'YYYY-MM-DD') AS update_date,
          item_number,
          item_name,
          cost_per_item,
          number_of_items,
          current_price,
          total_cost,
          total_value,
          item_link,
          "buy_date",
          purchase_info,
         real_cost_per_item,
         real_total_cost
        FROM inventory i;
          """)
      # Update inventory_data with calculated values
        cursor.execute("""
         update inventory_data
              set exchange_rate = ct.rate
                  from currency_table ct
        where ct.date = inventory_data.buy_date
              AND inventory_data.exchange_rate IS NULL;
        """) 
        conn.commit()
        
        cursor.execute("""
         update inventory_data
           set exchange_rate_update = ct.rate
              from currency_table ct
           where ct.date = inventory_data.update_date
                AND inventory_data.exchange_rate_update IS NULL;
        """) 
        conn.commit()
        
        
        cursor.execute("""
         update inventory_data
              set type_of_purchase_channel = pc.type_of_channel
                  from purchase_channels pc
              where pc.id = inventory_data.purchase_id
                  and type_of_purchase_channel is null;
        """) 
        conn.commit()
        
        cursor.execute("""
         update inventory_data 
          set 
              cost_per_item_pln = cost_per_item * exchange_rate,
              current_price_pln = current_price * exchange_rate_update
          where inventory_data.cost_per_item_pln is null;
        """) 
        conn.commit()
        
        cursor.execute("""
         update inventory_data 
              set total_cost_pln = cost_per_item_pln * number_of_items,
              total_value_pln = number_of_items * current_price_pln
          where inventory_data.total_cost_pln is null;
        """) 
        conn.commit()
        
        cursor.execute("""
         update inventory_data 
              set real_total_value_pln = total_value_pln * 0.65
              where inventory_data.real_total_value_pln is null;
        """) 
        conn.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
