from tkinter import *
from tkinter import messagebox, ttk
import os

class LoginScreen:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        master.geometry("400x300")
        master.configure(bg='#E8F0FE')

        Label(master, text="Pharmacy Management System", font=("Poppins", 16, "bold"), bg='#E8F0FE').pack(pady=10)
        
        self.label_username = Label(master, text="Username:", font=("Arial", 12), bg='#E8F0FE')
        self.label_username.pack(pady=5)
        self.entry_username = Entry(master, font=("Arial", 12))
        self.entry_username.pack(pady=5)

        self.label_password = Label(master, text="Password:", font=("Arial", 12), bg='#E8F0FE')
        self.label_password.pack(pady=5)
        self.entry_password = Entry(master, show="*", font=("Arial", 12))
        self.entry_password.pack(pady=5)

        self.button_login = Button(master, text="Login", font=("Arial", 12), bg='#007BFF', fg='white', command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "LOKESH" and password == "lokesh07":
            self.master.destroy()
            root = Tk()
            app = PharmacyManagementSystem(root)
            root.mainloop()
        else:
            messagebox.showerror("Login Error", "Invalid Username or Password!")

class PharmacyManagementSystem:
    def __init__(self, master):
        self.master = master
        master.title("Pharmacy Management System")
        master.geometry("900x600")
        master.configure(bg='#E8F0FE')

        # Create Tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=BOTH, expand=True)

        # Add Tablet Tab
        self.add_tablet_tab = Frame(self.notebook, bg='#E8F0FE')
        self.notebook.add(self.add_tablet_tab, text="Add Tablet")

        # Inventory Tab
        self.inventory_tab = Frame(self.notebook, bg='#E8F0FE')
        self.notebook.add(self.inventory_tab, text="Inventory")

        # Billing Tab
        self.billing_tab = Frame(self.notebook, bg='#E8F0FE')
        self.notebook.add(self.billing_tab, text="Billing")

        # Database File
        self.DB_FILE = "pharmacy_database.txt"
        if not os.path.exists(self.DB_FILE):
            open(self.DB_FILE, 'a').close()

        self.create_add_tablet_tab()
        self.create_inventory_tab()
        self.create_billing_tab()

    def create_add_tablet_tab(self):
        Label(self.add_tablet_tab, text="Add New Tablet", font=("Arial", 14), bg='#E8F0FE').grid(row=0, column=0, columnspan=2, pady=10)

        Label(self.add_tablet_tab, text="Tablet Name:", bg='#E8F0FE').grid(row=1, column=0, padx=10, pady=5)
        self.entry_name = Entry(self.add_tablet_tab)
        self.entry_name.grid(row=1, column=1, padx=10, pady=5)

        Label(self.add_tablet_tab, text="Quantity:", bg='#E8F0FE').grid(row=2, column=0, padx=10, pady=5)
        self.entry_quantity = Entry(self.add_tablet_tab)
        self.entry_quantity.grid(row=2, column=1, padx=10, pady=5)

        Label(self.add_tablet_tab, text="Price per Tablet:", bg='#E8F0FE').grid(row=3, column=0, padx=10, pady=5)
        self.entry_price = Entry(self.add_tablet_tab)
        self.entry_price.grid(row=3, column=1, padx=10, pady=5)

        Label(self.add_tablet_tab, text="Rack:", bg='#E8F0FE').grid(row=4, column=0, padx=10, pady=5)
        self.entry_rack = Entry(self.add_tablet_tab)
        self.entry_rack.grid(row=4, column=1, padx=10, pady=5)

        Button(self.add_tablet_tab, text="Add Tablet", bg='#007BFF', fg='white', command=self.add_tablet).grid(row=5, columnspan=2, pady=10)

    def add_tablet(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        rack = self.entry_rack.get()

        if name and quantity.isdigit() and price.replace('.', '', 1).isdigit() and rack:
            with open(self.DB_FILE, 'a') as f:
                f.write(f"{name},{quantity},{price},{rack}\n")
            messagebox.showinfo("Success", "Tablet added successfully!")
            self.clear_add_tablet_entries()
            self.view_tablets()  # Refresh inventory view
        else:
            messagebox.showwarning("Invalid Input", "Please fill in all fields with valid data.")

    def clear_add_tablet_entries(self):
        self.entry_name.delete(0, END)
        self.entry_quantity.delete(0, END)
        self.entry_price.delete(0, END)
        self.entry_rack.delete(0, END)

    def create_inventory_tab(self):
        Label(self.inventory_tab, text="Tablet Inventory", font=("Arial", 14), bg='#E8F0FE').pack(pady=10)
        
        search_frame = Frame(self.inventory_tab, bg='#E8F0FE')
        search_frame.pack(pady=10)
        Label(search_frame, text="Search by Name:", bg='#E8F0FE').pack(side=LEFT, padx=5)
        self.search_entry = Entry(search_frame)
        self.search_entry.pack(side=LEFT, padx=5)
        Button(search_frame, text="Search", command=self.search_tablet).pack(side=LEFT, padx=5)

        # Treeview for displaying tablets
        self.treeview = ttk.Treeview(self.inventory_tab, columns=('Name', 'Quantity', 'Price', 'Rack'), show='headings')
        self.treeview.heading('Name', text='Name')
        self.treeview.heading('Quantity', text='Quantity')
        self.treeview.heading('Price', text='Price')
        self.treeview.heading('Rack', text='Rack')
        self.treeview.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.view_tablets()

    def search_tablet(self):
        search_name = self.search_entry.get().strip().lower()
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        with open(self.DB_FILE, 'r') as f:
            for line in f:
                name, quantity, price, rack = line.strip().split(',')
                if search_name in name.lower():
                    self.treeview.insert('', 'end', values=(name, quantity, price, rack))

    def view_tablets(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        with open(self.DB_FILE, 'r') as f:
            for line in f:
                name, quantity, price, rack = line.strip().split(',')
                self.treeview.insert('', 'end', values=(name, quantity, price, rack))

    def create_billing_tab(self):
        Label(self.billing_tab, text="Billing", font=("Arial", 14), bg='#E8F0FE').pack(pady=10)

        Label(self.billing_tab, text="Tablet Name:", bg='#E8F0FE').pack(pady=5)
        self.billing_name = Entry(self.billing_tab)
        self.billing_name.pack(pady=5)

        Label(self.billing_tab, text="Quantity:", bg='#E8F0FE').pack(pady=5)
        self.billing_quantity = Entry(self.billing_tab)
        self.billing_quantity.pack(pady=5)

        Button(self.billing_tab, text="Calculate Bill", bg='#007BFF', fg='white', command=self.generate_bill).pack(pady=10)
        self.billing_total = Label(self.billing_tab, text="Total: $0.00", font=("Arial", 12), bg='#E8F0FE')
        self.billing_total.pack(pady=5)

    def generate_bill(self):
        name = self.billing_name.get()
        quantity = self.billing_quantity.get()
        
        if quantity.isdigit():
            quantity = int(quantity)
            total_price = 0

            with open(self.DB_FILE, 'r') as f:
                for line in f:
                    tablet_name, qty, price, rack = line.strip().split(',')
                    if tablet_name.lower() == name.lower():
                        total_price = quantity * float(price)
                        break
            self.billing_total.config(text=f"Total: ${total_price:.2f}")
        else:
            messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity.")

root = Tk()
app = LoginScreen(root)
root.mainloop()
