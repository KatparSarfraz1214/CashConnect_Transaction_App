CashConnect – A Python Transaction Application 
CashConnect is a beginner-friendly yet professionally structured desktop transaction application built using Python and Tkinter. It simulates a simple digital banking system where users can securely manage accounts, perform transactions, and view transaction history.

Project Overview
CashConnect allows users to:
- Create accounts with username + secure 4-digit PIN
- Log in securely using PIN authentication
- View real-time account balance
- Deposit money
- Withdraw money
- Transfer money between users
- View full transaction history
- View recent transactions on dashboard

Key Features
1. Security
- PIN-based authentication (4-digit PIN per user)
- Login validation before accessing dashboard

2. User Interface
- Built using Tkinter
- Full-screen dashboard optimized for PC/Laptop screens
- Each operation (Deposit, Withdraw, Transfer, History) opens in a new full-screen window
- Clean layout with colors and readable fonts
- Transaction Management
- Real-time balance updates
- Stores complete transaction history
- Displays last 5 transactions on dashboard
- Time-stamped transactions using datetime

3. Data Handling
- Uses Python dictionaries for account data
- Uses lists for transaction logs
- No external database (lightweight & simple)

4. Technologies Used

Python 3.x as core programming language
Tkinter	framework for GUI development
datetime	Timestamping transactions
Standard Python Libraries	No external dependencies
