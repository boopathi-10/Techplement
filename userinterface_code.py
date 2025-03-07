import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

CONTACTS_FILE = "contacts.json"


def load_contacts():
    try:
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)


def add_contact():
    name = simpledialog.askstring("Input", "Enter name:")
    phone = simpledialog.askstring("Input", "Enter phone number:")
    email = simpledialog.askstring("Input", "Enter email:")

    if name and phone and email:
        contacts = load_contacts()
        contacts.append({"name": name, "phone": phone, "email": email})
        save_contacts(contacts)
        messagebox.showinfo("Success", "Contact added successfully!")
        view_contacts()
    else:
        messagebox.showwarning("Input Error", "All fields are required!")


def view_contacts():
    contacts = load_contacts()
    for row in tree.get_children():
        tree.delete(row)
    for contact in contacts:
        tree.insert("", tk.END, values=(contact['name'], contact['phone'], contact['email']))


def search_contact():
    search_term = simpledialog.askstring("Search", "Enter name or phone:")
    contacts = load_contacts()
    results = [c for c in contacts if search_term in c["name"] or search_term in c["phone"]]

    for row in tree.get_children():
        tree.delete(row)
    if results:
        for contact in results:
            tree.insert("", tk.END, values=(contact['name'], contact['phone'], contact['email']))
    else:
        messagebox.showinfo("No Results", "No contacts found.")


def update_contact():
    name = simpledialog.askstring("Update", "Enter the name of the contact to update:")
    contacts = load_contacts()

    for contact in contacts:
        if contact["name"] == name:
            contact["phone"] = simpledialog.askstring("Update", "Enter new phone number:") or contact["phone"]
            contact["email"] = simpledialog.askstring("Update", "Enter new email:") or contact["email"]
            save_contacts(contacts)
            messagebox.showinfo("Success", "Contact updated successfully!")
            view_contacts()
            return
    messagebox.showerror("Error", "Contact not found.")


def delete_contact():
    name = simpledialog.askstring("Delete", "Enter the name of the contact to delete:")
    contacts = load_contacts()
    contacts = [c for c in contacts if c["name"] != name]
    save_contacts(contacts)
    messagebox.showinfo("Success", "Contact deleted successfully!")
    view_contacts()


# Create main GUI window
root = tk.Tk()
root.title("Contact Management System")
root.geometry("600x450")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root)
frame.pack(pady=20)

tree = ttk.Treeview(frame, columns=("Name", "Phone", "Email"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")

# Center align text in columns
tree.column("Name", anchor="center")
tree.column("Phone", anchor="center")
tree.column("Email", anchor="center")

tree.pack(pady=10, fill=tk.BOTH, expand=True)

btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

btn_add = tk.Button(btn_frame, text="Add Contact", command=add_contact, bg="#4CAF50", fg="white", padx=10, pady=5)
btn_add.grid(row=0, column=0, padx=5)

btn_view = tk.Button(btn_frame, text="View Contacts", command=view_contacts, bg="#2196F3", fg="white", padx=10, pady=5)
btn_view.grid(row=0, column=1, padx=5)

btn_search = tk.Button(btn_frame, text="Search Contact", command=search_contact, bg="#FFC107", fg="black", padx=10,
                       pady=5)
btn_search.grid(row=0, column=2, padx=5)

btn_update = tk.Button(btn_frame, text="Update Contact", command=update_contact, bg="#FF9800", fg="white", padx=10,
                       pady=5)
btn_update.grid(row=0, column=3, padx=5)

btn_delete = tk.Button(btn_frame, text="Delete Contact", command=delete_contact, bg="#F44336", fg="white", padx=10,
                       pady=5)
btn_delete.grid(row=0, column=4, padx=5)

btn_exit = tk.Button(root, text="Exit", command=root.quit, bg="#9E9E9E", fg="white", padx=10, pady=5)
btn_exit.pack(pady=10)

view_contacts()
root.mainloop()