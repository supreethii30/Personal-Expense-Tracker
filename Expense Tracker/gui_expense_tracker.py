import tkinter as tk
from tkinter import ttk, messagebox
import csv
import datetime
import calendar
from expense import Expense  # reuse your class

EXPENSE_FILE = "expense.csv"
BUDGET = 10000

# ---------------- SAVE EXPENSE ----------------
def save_expense():
    name = name_entry.get()
    amount = amount_entry.get()
    category = category_var.get()

    if not name or not amount:
        messagebox.showwarning("Input Error", "Please enter all fields")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    expense = Expense(name=name, category=category, amount=amount)

    with open(EXPENSE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([expense.name, expense.category, expense.amount])

    messagebox.showinfo("Saved", f"Expense '{name}' added successfully!")
    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# ---------------- SHOW SUMMARY ----------------
def show_summary():
    expenses = []
    try:
        with open(EXPENSE_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    expenses.append(Expense(row[0], row[1], float(row[2])))
    except FileNotFoundError:
        messagebox.showerror("Error", "No expenses found yet!")
        return

    total_spent = sum(e.amount for e in expenses)
    remaining_budget = BUDGET - total_spent

    # remaining days in month
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0

    summary_text = (
        f"Total Spent: ₹{total_spent:.2f}\n"
        f"Remaining Budget: ₹{remaining_budget:.2f}\n"
        f"Remaining Days: {remaining_days}\n"
        f"Daily Budget: ₹{daily_budget:.2f}"
    )

    messagebox.showinfo("Expense Summary", summary_text)

# ---------------- GUI LAYOUT ----------------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x300")

# Name
tk.Label(root, text="Expense Name:").pack(pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack()

# Amount
tk.Label(root, text="Expense Amount:").pack(pady=5)
amount_entry = tk.Entry(root, width=30)
amount_entry.pack()

# Category
tk.Label(root, text="Category:").pack(pady=5)
category_var = tk.StringVar()
categories = ["🍔 Food", "🏠 Home", "🏙️ Work", "🎉 Entertainment", "😃 Beauty Expenses"]
category_dropdown = ttk.Combobox(root, textvariable=category_var, values=categories)
category_dropdown.current(0)
category_dropdown.pack()

# Buttons
tk.Button(root, text="Add Expense", command=save_expense, bg="lightgreen").pack(pady=10)
tk.Button(root, text="Show Summary", command=show_summary, bg="lightblue").pack(pady=10)

root.mainloop()
