import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector
from tkinter import messagebox
from datetime import datetime
from decimal import Decimal


# Module 1: Database Connection
def create_connection():
    conn = mysql.connector.connect(host='localhost', user='root', password='yourpwd')
    cursor = conn.cursor()

    # Create the 'bank' database

    cursor.execute('CREATE DATABASE IF NOT EXISTS bank')
    
    conn = mysql.connector.connect(host='localhost', user='root', password='yourpwd',db = 'bank')

    cursor = conn.cursor()
    # Switch to the 'bank' database

    # Create the 'accounts' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INT AUTO_INCREMENT PRIMARY KEY,
            account_name VARCHAR(255) NOT NULL,
            balance DECIMAL(10, 2) NOT NULL
        )
    """)

    

# Create the 'transactions' table with a foreign key constraint
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            account_number INT,
            transaction_type VARCHAR(255) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            transaction_date DATETIME NOT NULL,
            FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        )
    """)



        

    conn.commit()
    conn.close()


# Module 3: Account Creation GUI
def create_account_gui():
    account_window = tk.Toplevel(root)
    account_window.title("Create Account")

    ttk.Label(account_window, text="Account Name:").pack()
    account_name_entry = ttk.Entry(account_window)
    account_name_entry.pack()

    ttk.Label(account_window, text="Initial Balance:").pack()
    initial_balance_entry = ttk.Entry(account_window)
    initial_balance_entry.pack()

    ttk.Button(account_window, text="Create Account", command=lambda: create_account(account_name_entry.get(), initial_balance_entry.get())).pack()

# Module 4: Deposit GUI
def deposit_gui():
    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit Money")

    ttk.Label(deposit_window, text="Account Number:").pack()
    account_number_entry = ttk.Entry(deposit_window)
    account_number_entry.pack()

    ttk.Label(deposit_window, text="Deposit Amount:").pack()
    deposit_amount_entry = ttk.Entry(deposit_window)
    deposit_amount_entry.pack()

    ttk.Button(deposit_window, text="Deposit", command=lambda: deposit_money(account_number_entry.get(), deposit_amount_entry.get())).pack()

# Module 5: Withdraw GUI
def withdraw_gui():
    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw Money")

    ttk.Label(withdraw_window, text="Account Number:").pack()
    account_number_entry = ttk.Entry(withdraw_window)
    account_number_entry.pack()

    ttk.Label(withdraw_window, text="Withdrawal Amount:").pack()
    withdrawal_amount_entry = ttk.Entry(withdraw_window)
    withdrawal_amount_entry.pack()

    ttk.Button(withdraw_window, text="Withdraw", command=lambda: withdraw_money(account_number_entry.get(), withdrawal_amount_entry.get())).pack()

# Module 6: Balance Inquiry GUI
def balance_inquiry_gui():
    balance_window = tk.Toplevel(root)
    balance_window.title("Balance Inquiry")

    ttk.Label(balance_window, text="Account Number:").pack()
    account_number_entry = ttk.Entry(balance_window)
    account_number_entry.pack()

    ttk.Button(balance_window, text="Check Balance", command=lambda: check_balance(account_number_entry.get())).pack()

# Module 7: Transaction History GUI
def transaction_history_gui():
    history_window = tk.Toplevel(root)
    history_window.title("Transaction History")

    ttk.Label(history_window, text="Account Number:").pack()
    account_number_entry = ttk.Entry(history_window)
    account_number_entry.pack()

    ttk.Button(history_window, text="View History", command=lambda: view_transaction_history(account_number_entry.get())).pack()

# Module 8: Create Account
def create_account(account_name, initial_balance):
    try:
        initial_balance = float(initial_balance)
    except ValueError:
        messagebox.showerror("Error", "Invalid initial balance")
        return

    conn = mysql.connector.connect(host='localhost', user='root', password='@pPu2005',db = 'bank')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO accounts (account_name, balance) VALUES (%s, %s)", (account_name, initial_balance))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Account created successfully!")

# Module 9: Deposit Money
def deposit_money(account_number, amount):
    try:
        account_number = int(account_number)
        amount = Decimal(amount)  # Convert amount to Decimal
    except ValueError:
        messagebox.showerror("Error", "Invalid account number or amount")
        return

    conn = mysql.connector.connect(host='localhost', user='root', password='@pPu2005',db = 'bank')
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()

    if result:
        balance = Decimal(result[0])  # Convert balance to Decimal
        new_balance = balance + amount
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
        cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount, transaction_date) VALUES (%s, %s, %s, %s)",
                       (account_number, "Deposit", amount, datetime.now()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Deposited {amount} successfully!")
    else:
        conn.close()
        messagebox.showerror("Error", "Account not found")



# Module 10: Withdraw Money
def withdraw_money(account_number, amount):
    try:
        account_number = int(account_number)
        amount = Decimal(amount)  # Convert amount to Decimal
    except ValueError:
        messagebox.showerror("Error", "Invalid account number or amount")
        return

    conn  = mysql.connector.connect(host='localhost', user='root', password='@pPu2005',db = 'bank')
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()

    if result:
        balance = Decimal(result[0])  # Convert balance to Decimal
        if balance >= amount:
            new_balance = balance - amount
            cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
            cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount, transaction_date) VALUES (%s, %s, %s, %s)",
                           (account_number, "Withdrawal", amount, datetime.now()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Withdrew {amount} successfully!")
        else:
            conn.close()
            messagebox.showerror("Error", "Insufficient balance")
    else:
        conn.close()
        messagebox.showerror("Error", "Account not found")


# Module 11: Balance Inquiry
def check_balance(account_number):
    try:
        account_number = int(account_number)
    except ValueError:
        messagebox.showerror("Error", "Invalid account number")
        return

    conn = mysql.connector.connect(host='localhost', user='root', password='@pPu2005',db = 'bank')
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        messagebox.showinfo("Balance", f"Account balance: {balance}")
    else:
        conn.close()
        messagebox.showerror("Error", "Account not found")

# Module 12: Transaction History
def view_transaction_history(account_number):
    try:
        account_number = int(account_number)
    except ValueError:
        messagebox.showerror("Error", "Invalid account number")
        return

    conn = mysql.connector.connect(host='localhost', user='root', password='@pPu2005',db = 'bank')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE account_number = %s", (account_number,))
    result = cursor.fetchall()

    if result:
        history_window = tk.Toplevel(root)
        history_window.title("Transaction History")

        history_text = tk.Text(history_window)
        history_text.pack()

        history_text.insert(tk.END, "Transaction History:\n")
        for row in result:
            transaction_id, account_number, transaction_type, amount, transaction_date = row
            history_text.insert(tk.END, f"Transaction ID: {transaction_id}\n")
            history_text.insert(tk.END, f"Account Number: {account_number}\n")
            history_text.insert(tk.END, f"Transaction Type: {transaction_type}\n")
            history_text.insert(tk.END, f"Amount: {amount}\n")
            history_text.insert(tk.END, f"Date: {transaction_date}\n")
            history_text.insert(tk.END, "\n")

        history_text.config(state=tk.DISABLED)
    else:
        conn.close()
        messagebox.showerror("Error", "No transaction history found for this account")

# Module 13: Main GUI
root = tk.Tk()
root.title("Banking Management System")

# Create and place labels, buttons, and entry fields for the main GUI
ttk.Button(root, text="Create Account", command=create_account_gui).pack()
ttk.Button(root, text="Deposit Money", command=deposit_gui).pack()
ttk.Button(root, text="Withdraw Money", command=withdraw_gui).pack()
ttk.Button(root, text="Balance Inquiry", command=balance_inquiry_gui).pack()
ttk.Button(root, text="Transaction History", command=transaction_history_gui).pack()

create_connection()
# Module 14: Main Application Loop
root.mainloop()

