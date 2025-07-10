import sqlite3

connect = sqlite3.connect('FinanceManager.db')
cursor = connect.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    category TEXT,       
    amount REAL,         
    date TEXT,           
)
''')

connect.commit()
connect.close()

def add_transaction(type, category, amount, date):
    connect = sqlite3.connect('FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('''
    INSERT INTO transactions (type, category, amount, date)
    VALUES (?, ?, ?, ?)
    ''', (type, category, amount, date))
    connect.commit()
    connect.close()

def view_transactions():
    connect = sqlite3.connect('FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    connect.close()
    return transactions
    
def remove_transaction(id):
    connect = sqlite3.connect('FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (id))  
    connect.commit()
    connect.close()

def view_category(category):
    connect = sqlite3.connect('FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('SELECT FROM transactions WHERE category = ?', (category))
    transactions = cursor.fetchall()
    connect.commit()
    connect.close()
    return transactions

def spent_category(category):
    connect = sqlite3.connect('FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('SELECT amount FROM transactions WHERE category = ? AND type = "expense"' , (category))
    transactions = cursor.fetchall()
    total = sum(transaction[0] for transaction in transactions)
    connect.commit()
    connect.close()
    return total