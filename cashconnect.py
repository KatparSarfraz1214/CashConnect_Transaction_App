# CashConnect: A Transaction Application (PIN + Fullscreen Dashboard)
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# -----------------------
# Data Storage
# -----------------------
# Structure: accounts = {username: {"balance": float, "pin": str}}
accounts = {}
transactions = {}

# -----------------------
# Utility Functions
# -----------------------
def add_transaction(username, type_, amount, target=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"type": type_, "amount": amount, "time": now}
    if type_ in ["Transfer", "Received"]:
        entry["target"] = target
    transactions[username].append(entry)

def create_account(username, pin, initial_balance):
    if username in accounts:
        return False, "Username already exists."
    if initial_balance < 0:
        return False, "Balance cannot be negative."
    accounts[username] = {"balance": initial_balance, "pin": pin}
    transactions[username] = []
    return True, "Account created successfully!"

def deposit(username, amount):
    if amount <= 0:
        return False, "Deposit amount must be positive."
    accounts[username]["balance"] += amount
    add_transaction(username, "Deposit", amount)
    return True, f"Deposited ${amount:.2f} successfully!"

def withdraw(username, amount):
    if amount <= 0:
        return False, "Withdrawal amount must be positive."
    if accounts[username]["balance"] < amount:
        return False, "Insufficient balance."
    accounts[username]["balance"] -= amount
    add_transaction(username, "Withdraw", amount)
    return True, f"Withdrew ${amount:.2f} successfully!"

def transfer(sender, receiver, amount):
    if receiver not in accounts:
        return False, "Receiver does not exist."
    if amount <= 0:
        return False, "Transfer amount must be positive."
    if accounts[sender]["balance"] < amount:
        return False, "Insufficient balance."
    accounts[sender]["balance"] -= amount
    accounts[receiver]["balance"] += amount
    add_transaction(sender, "Transfer", amount, target=receiver)
    add_transaction(receiver, "Received", amount, target=sender)
    return True, f"Transferred ${amount:.2f} to {receiver} successfully!"

# -----------------------
# GUI Functions
# -----------------------
def show_transaction_history(username):
    win = tk.Toplevel()
    win.title(f"{username} - Transaction History")
    win.state('zoomed')  # Fullscreen
    win.configure(bg="#f0f0f0")

    tk.Label(win, text=f"{username}'s Transaction History", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    history_list = tk.Listbox(win, font=("Arial", 12))
    history_list.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    user_transactions = transactions.get(username, [])
    if not user_transactions:
        history_list.insert(tk.END, "No transactions yet.")
    else:
        for t in user_transactions:
            if t["type"] in ["Transfer", "Received"]:
                history_list.insert(tk.END, f"{t['time']}: {t['type']} ${t['amount']:.2f} with {t.get('target','')}")
            else:
                history_list.insert(tk.END, f"{t['time']}: {t['type']} ${t['amount']:.2f}")

def deposit_window(username, balance_label, recent_list):
    win = tk.Toplevel()
    win.title("Deposit Money")
    win.state('zoomed')
    win.configure(bg="#d1f0d1")

    tk.Label(win, text="Enter amount to deposit:", font=("Arial", 14), bg="#d1f0d1").pack(pady=10)
    amount_entry = tk.Entry(win, font=("Arial", 14))
    amount_entry.pack(pady=10)

    def perform_deposit():
        try:
            amt = float(amount_entry.get())
            success, msg = deposit(username, amt)
            messagebox.showinfo("Deposit", msg)
            if success:
                balance_label.config(text=f"Balance: ${accounts[username]['balance']:.2f}")
                update_recent_transactions(username, recent_list)
                win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    tk.Button(win, text="Deposit", bg="#4CAF50", fg="white", font=("Arial", 14), command=perform_deposit).pack(pady=20)

def withdraw_window(username, balance_label, recent_list):
    win = tk.Toplevel()
    win.title("Withdraw Money")
    win.state('zoomed')
    win.configure(bg="#f0d1d1")

    tk.Label(win, text="Enter amount to withdraw:", font=("Arial", 14), bg="#f0d1d1").pack(pady=10)
    amount_entry = tk.Entry(win, font=("Arial", 14))
    amount_entry.pack(pady=10)

    def perform_withdraw():
        try:
            amt = float(amount_entry.get())
            success, msg = withdraw(username, amt)
            messagebox.showinfo("Withdraw", msg)
            if success:
                balance_label.config(text=f"Balance: ${accounts[username]['balance']:.2f}")
                update_recent_transactions(username, recent_list)
                win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    tk.Button(win, text="Withdraw", bg="#f44336", fg="white", font=("Arial", 14), command=perform_withdraw).pack(pady=20)

def transfer_window(username, balance_label, recent_list):
    win = tk.Toplevel()
    win.title("Transfer Money")
    win.state('zoomed')
    win.configure(bg="#d1d1f0")

    tk.Label(win, text="Enter recipient username:", font=("Arial", 14), bg="#d1d1f0").pack(pady=10)
    receiver_entry = tk.Entry(win, font=("Arial", 14))
    receiver_entry.pack(pady=10)

    tk.Label(win, text="Enter amount to transfer:", font=("Arial", 14), bg="#d1d1f0").pack(pady=10)
    amount_entry = tk.Entry(win, font=("Arial", 14))
    amount_entry.pack(pady=10)

    def perform_transfer():
        receiver = receiver_entry.get()
        try:
            amt = float(amount_entry.get())
            success, msg = transfer(username, receiver, amt)
            messagebox.showinfo("Transfer", msg)
            if success:
                balance_label.config(text=f"Balance: ${accounts[username]['balance']:.2f}")
                update_recent_transactions(username, recent_list)
                win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")

    tk.Button(win, text="Transfer", bg="#2196F3", fg="white", font=("Arial", 14), command=perform_transfer).pack(pady=20)

def update_recent_transactions(username, recent_list):
    recent_list.delete(0, tk.END)
    user_transactions = transactions.get(username, [])
    recent_list.insert(tk.END, "Last 5 Transactions:")
    if not user_transactions:
        recent_list.insert(tk.END, "No transactions yet.")
    else:
        for t in user_transactions[-5:][::-1]:
            if t["type"] in ["Transfer", "Received"]:
                recent_list.insert(tk.END, f"{t['type']} ${t['amount']:.2f} with {t.get('target','')}")
            else:
                recent_list.insert(tk.END, f"{t['type']} ${t['amount']:.2f}")

def dashboard(username):
    dash_win = tk.Toplevel()
    dash_win.title(f"CashConnect Dashboard - {username}")
    dash_win.state('zoomed')  # Fullscreen
    dash_win.configure(bg="#fffacd")

    tk.Label(dash_win, text=f"Welcome, {username}", font=("Arial", 20, "bold"), bg="#fffacd").pack(pady=10)

    balance_frame = tk.Frame(dash_win, bg="#fffacd")
    balance_frame.pack(pady=10)
    balance_label = tk.Label(balance_frame, text=f"Balance: ${accounts[username]['balance']:.2f}", font=("Arial", 18), bg="#fffacd")
    balance_label.pack()

    button_frame = tk.Frame(dash_win, bg="#fffacd")
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="Deposit Money", width=20, bg="#4CAF50", fg="white", font=("Arial", 14),
              command=lambda: deposit_window(username, balance_label, recent_list)).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="Withdraw Money", width=20, bg="#f44336", fg="white", font=("Arial", 14),
              command=lambda: withdraw_window(username, balance_label, recent_list)).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(button_frame, text="Transfer Money", width=20, bg="#2196F3", fg="white", font=("Arial", 14),
              command=lambda: transfer_window(username, balance_label, recent_list)).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="Transaction History", width=20, bg="#FF9800", fg="white", font=("Arial", 14),
              command=lambda: show_transaction_history(username)).grid(row=1, column=1, padx=10, pady=10)

    # Recent Transactions
    recent_frame = tk.Frame(dash_win, bg="#fffacd")
    recent_frame.pack(pady=20, fill=tk.BOTH, expand=True)
    recent_list = tk.Listbox(recent_frame, width=80, height=8, font=("Arial", 12))
    recent_list.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    update_recent_transactions(username, recent_list)

    # All accounts summary (for demo)
    summary_frame = tk.Frame(dash_win, bg="#fffacd")
    summary_frame.pack(pady=20, fill=tk.BOTH)
    summary_list = tk.Listbox(summary_frame, width=80, height=5, font=("Arial", 12))
    summary_list.pack(padx=20, pady=10, fill=tk.BOTH)
    summary_list.insert(tk.END, "All Accounts Summary (Demo):")
    for user, info in accounts.items():
        summary_list.insert(tk.END, f"{user}: ${info['balance']:.2f}")

# -----------------------
# Login and Account Creation
# -----------------------
def main_window():
    root = tk.Tk()
    root.title("CashConnect")
    root.state('zoomed')
    root.configure(bg="#e6f2ff")

    tk.Label(root, text="CashConnect Transaction App", font=("Arial", 20, "bold"), fg="#ff8c00", bg="#e6f2ff").pack(pady=20)

    tk.Label(root, text="Username:", font=("Arial", 14), bg="#e6f2ff").pack(pady=5)
    username_entry = tk.Entry(root, font=("Arial", 14))
    username_entry.pack(pady=5)

    tk.Label(root, text="PIN (4 digits):", font=("Arial", 14), bg="#e6f2ff").pack(pady=5)
    pin_entry = tk.Entry(root, show="*", font=("Arial", 14))
    pin_entry.pack(pady=5)

    tk.Label(root, text="Initial Balance (new account):", font=("Arial", 14), bg="#e6f2ff").pack(pady=5)
    balance_entry = tk.Entry(root, font=("Arial", 14))
    balance_entry.pack(pady=5)

    def create_new_account():
        username = username_entry.get().strip()
        pin = pin_entry.get().strip()
        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be 4 digits.")
            return
        try:
            balance = float(balance_entry.get())
            success, msg = create_account(username, pin, balance)
            messagebox.showinfo("Account Creation", msg)
            if success:
                dashboard(username)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid initial balance.")

    def login_account():
        username = username_entry.get().strip()
        pin = pin_entry.get().strip()
        if username in accounts and accounts[username]["pin"] == pin:
            dashboard(username)
        else:
            messagebox.showerror("Login Failed", "Incorrect username or PIN.")

    tk.Button(root, text="Create Account", width=25, bg="#4CAF50", fg="white", font=("Arial", 14), command=create_new_account).pack(pady=10)
    tk.Button(root, text="Login", width=25, bg="#2196F3", fg="white", font=("Arial", 14), command=login_account).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()
