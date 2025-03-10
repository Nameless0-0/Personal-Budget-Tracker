import tkinter as tk
from tkinter import messagebox, StringVar, filedialog
import json
import os

class BudgetTracker:
    def __init__(self, filename='budget.json'):
        self.filename = filename
        self.data = {"income": 0, "expenses": []}  # Initialize income and expenses
        self.load_data()  # Load existing data if available

    def load_data(self):
        """Load budget data from a JSON file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.data = json.load(file)

    def save_data(self):
        """Save current budget data to a JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def add_income(self, amount):
        """Add income and save the updated data."""
        self.data['income'] += amount
        self.save_data()

    def add_expense(self, description, amount, category='Other'):
        """Add an expense and save the updated data."""
        self.data['expenses'].append({
            "description": description,
            "amount": amount,
            "category": category
        })
        self.save_data()

    def clear_history(self):
        """Clear all income and expenses and save the changes."""
        self.data['income'] = 0
        self.data['expenses'] = []
        self.save_data()

class App:
    def __init__(self, root):
        self.tracker = BudgetTracker()  # Initialize the budget tracker
        self.root = root
        self.root.title("Personal Budget Tracker")
        self.root.geometry("650x700")

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        # Create and store each page/frame of the application
        for F in (HomePage, IncomePage, ExpensePage, SummaryPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")  # Show the home page initially

    def show_frame(self, page_name):
        """Raise the specified frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to Budget Tracker", font=("Courier New", 24))
        label.pack(pady=30)
        # Buttons to navigate to other pages
        button1 = tk.Button(self, text="Add Income", command=lambda: controller.show_frame("IncomePage"), font=("Courier New", 16))
        button1.pack(pady=10)
        button2 = tk.Button(self, text="Add Expense", command=lambda: controller.show_frame("ExpensePage"), font=("Courier New", 16))
        button2.pack(pady=10)
        button3 = tk.Button(self, text="View Summary", command=lambda: controller.show_frame("SummaryPage"), font=("Courier New", 16))
        button3.pack(pady=10)

class IncomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Add Income", font=("Courier New", 24))
        label.pack(pady=30)
        self.income_entry = tk.Entry(self, font=("Courier New", 16))
        self.income_entry.pack(pady=10)
        add_income_btn = tk.Button(self, text="Add Income", command=self.add_income, font=("Courier New", 16))
        add_income_btn.pack(pady=10)
        back_btn = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), font=("Courier New", 16))
        back_btn.pack(pady=10)

    def add_income(self):
        """Validate and add income to the tracker."""
        try:
            amount = float(self.income_entry.get())
            if amount < 0:
                raise ValueError("Negative value")
            self.controller.tracker.add_income(amount)
            messagebox.showinfo("Success", "Income added successfully!")
            self.income_entry.delete(0, tk.END)  # Clear the entry field
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")

class ExpensePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Add Expense", font=("Courier New", 24))
        label.pack(pady=30)

        # Expense description entry
        desc_label = tk.Label(self, text="Expense Description (e.g., dinner, movie tickets):", font=("Courier New", 16))
        desc_label.pack(pady=5)
        self.expense_desc_entry = tk.Entry(self, font=("Courier New", 16))
        self.expense_desc_entry.pack(pady=5)

        # Expense amount entry
        amount_label = tk.Label(self, text="Expense Amount ($):", font=("Courier New", 16))
        amount_label.pack(pady=5)
        self.expense_amount_entry = tk.Entry(self, font=("Courier New", 16))
        self.expense_amount_entry.pack(pady=5)

        # Category selection
        category_label = tk.Label(self, text="Expense Category:", font=("Courier New", 16))
        category_label.pack(pady=5)
        self.category_var = StringVar(self)
        self.category_var.set("Other")  # Default value
        categories = ["Food", "Rent", "Utilities", "Transport", "Entertainment", "Other"]
        
        self.category_menu = tk.OptionMenu(self, self.category_var, *categories)
        self.category_menu.config(font=("Courier New", 16))
        self.category_menu.pack(pady=5)

        add_expense_btn = tk.Button(self, text="Add Expense", command=self.add_expense, font=("Courier New", 16))
        add_expense_btn.pack(pady=10)
        back_btn = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), font=("Courier New", 16))
        back_btn.pack(pady=10)

    def add_expense(self):
        """Validate and add an expense to the tracker."""
        try:
            description = self.expense_desc_entry.get()
            amount = float(self.expense_amount_entry.get())
            if amount < 0:
                raise ValueError("Negative value")
            category = self.category_var.get()
            self.controller.tracker.add_expense(description, amount, category)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.expense_desc_entry.delete(0, tk.END)  # Clear the entry field
            self.expense_amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number.")

class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Budget Summary", font=("Courier New", 24))
        label.pack(pady=30)
        
        # Text area to display the summary
        self.summary_text = tk.Text(self, font=("Courier New", 12), height=15, width=60)
        self.summary_text.pack(pady=10)

        # Buttons for viewing, exporting, and clearing the summary
        view_summary_btn = tk.Button(self, text="View Summary", command=self.view_summary, font=("Courier New", 16))
        view_summary_btn.pack(pady=10)

        export_btn = tk.Button(self, text="Export Summary", command=self.export_summary, font=("Courier New", 16))
        export_btn.pack(pady=10)

        clear_history_btn = tk.Button(self, text="Clear History", command=self.clear_history, font=("Courier New", 16))
        clear_history_btn.pack(pady=10)

        back_btn = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("HomePage"), font=("Courier New", 16))
        back_btn.pack(pady=10)

    def view_summary(self):
        """Display the summary of income and expenses."""
        self.summary_text.delete(1.0, tk.END)  # Clear previous summary
        total_expenses = sum(expense['amount'] for expense in self.controller.tracker.data['expenses'])
        balance = self.controller.tracker.data['income'] - total_expenses
        
        category_totals = {}
        detailed_expenses = []

        for expense in self.controller.tracker.data['expenses']:
            category = expense.get('category', 'Other')
            category_totals[category] = category_totals.get(category, 0) + expense['amount']
            detailed_expenses.append(expense)

        # Construct the summary string
        summary = f"Total Income: ${self.controller.tracker.data['income']:.2f}\n" \
                  f"Total Expenses: ${total_expenses:.2f}\n" \
                  f"Balance: ${balance:.2f}\n\nExpenses by Category:\n"
        
        for category, total in category_totals.items():
            summary += f"- {category}: ${total:.2f}\n"

        summary += "\nDetailed Expenses:\n"
        for expense in detailed_expenses:
            summary += f"- {expense['description']} | ${expense['amount']:.2f} | Category: {expense['category']}\n"

        self.summary_text.insert(tk.END, summary)  # Display summary in text area

    def export_summary(self):
        """Export the summary to a text file."""
        summary = self.summary_text.get(1.0, tk.END).strip()
        if not summary:
            messagebox.showwarning("Warning", "Please view the summary before exporting.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(summary)  # Write summary to the file
            messagebox.showinfo("Success", "Summary exported successfully!")

    def clear_history(self):
        """Clear all expenses and reset income after confirmation."""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all expenses and reset the income?"):
            self.controller.tracker.clear_history()
            messagebox.showinfo("Success", "Expense history cleared successfully!")
            self.summary_text.delete(1.0, tk.END)  # Clear the summary text area

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)  # Initialize and run the application
    root.mainloop()