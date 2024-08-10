

import tkinter as tk
from tkinter import messagebox
import csv
import os

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beach Side Restaurant Menu")

        # Welcome message
        self.welcome_message = tk.Label(root, text="Welcome to Beach Side Restaurant!", font=("Helvetica", 16), fg="black")
        self.welcome_message.pack(pady=10)

        # Read menu from CSV
        file_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "dtcc", "finalprojmenu.csv")
        self.menu = self.read_menu_from_csv(file_path)

        # Display menu
        self.display_menu()

        # Initialize order
        self.order = {}

        # Item selection
        self.item_label = tk.Label(root, text="Item Number:")
        self.item_label.pack(pady=5)
        self.item_entry = tk.Entry(root)
        self.item_entry.pack(pady=5)

        self.quantity_label = tk.Label(root, text="Quantity:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.pack(pady=5)

        # Order button
        self.order_button = tk.Button(root, text="Add to Order", command=self.add_to_order)
        self.order_button.pack(pady=10)

        # Show Order button
        self.show_order_button = tk.Button(root, text="Show Order", command=self.show_order)
        self.show_order_button.pack(pady=10)

    def read_menu_from_csv(self, filename):
        menu = {}
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                item_number, item_name, price = row
                price = float(price.replace("$", "").strip())  # Remove currency symbol and whitespace
                menu[int(item_number)] = {"name": item_name, "price": price}
        return menu

    def display_menu(self):
        for item_number, item_info in self.menu.items():
            item_text = f"{item_number}. {item_info['name']} - ${item_info['price']:.2f}"
            tk.Label(self.root, text=item_text).pack()

    def add_to_order(self):
        try:
            item_number = int(self.item_entry.get())
            quantity = int(self.quantity_entry.get())
            if item_number in self.menu:
                item_info = self.menu[item_number]
                item_name = item_info['name']
                price = item_info['price']
                if item_name in self.order:
                    self.order[item_name]["quantity"] += quantity
                else:
                    self.order[item_name] = {"quantity": quantity, "price": price}
                messagebox.showinfo("Success", f"Added {quantity} {item_name}(s) to your order!")
            else:
                messagebox.showerror("Error", "Invalid item number!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid item number and quantity!")

    def show_order(self):
        order_summary = "Your Order:\n"
        total = 0
        for item_name, item_info in self.order.items():
            quantity = item_info["quantity"]
            price = item_info["price"]
            subtotal = price * quantity
            order_summary += f"{item_name}: {quantity} x ${price:.2f} = ${subtotal:.2f}\n"
            total += subtotal
        order_summary += f"\nGrand Total: ${total:.2f}"
        messagebox.showinfo("Your Order", order_summary)

if __name__ == "__main__":
    root = tk.Tk()
    menu_app = MenuApp(root)
    root.mainloop()
