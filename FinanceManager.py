import sqlite3

connect = sqlite3.connect('Finance-Manager-Project\FinanceManager.db')
cursor = connect.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            category TEXT,       
            amount REAL,         
            date DATE           
        )''')
connect.commit()
connect.close() 

def add_transaction(type, category, amount, date):
    if not (type == 'expense' or type == 'income'):
        raise ValueError("Type is not specified as income or expense")
    elif amount <= 0:
        raise ValueError("Amount must be positive")
    else:
        connect = sqlite3.connect('Finance-Manager-Project\FinanceManager.db')
        cursor = connect.cursor()
        cursor.execute('''
        INSERT INTO transactions (type, category, amount, date)
        VALUES (?, ?, ?, ?)
        ''', (type, category, amount, date))
        connect.commit()
        connect.close()

def select_all_transactions():
    connect = sqlite3.connect('Finance-Manager-Project\FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    connect.commit()
    connect.close()
    if not transactions:
        print("No expenses found")
    return transactions
    
def remove_transaction(id):
    connect = sqlite3.connect('Finance-Manager-Project\FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (id,))  
    connect.commit()
    connect.close()

def select_category(category):
    connect = sqlite3.connect('Finance-Manager-Project\FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM transactions WHERE category = ?', (category))
    transactions = cursor.fetchall()
    connect.commit()
    connect.close()
    if not transactions:
        print("No expenses found in " + category)
    return transactions

def spent_category(category):
    connect = sqlite3.connect('Finance-Manager-Project\FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('SELECT amount FROM transactions WHERE category = ? AND type = "expense"', (category,))
    transactions = cursor.fetchall()
    connect.commit()
    connect.close()
    if not transactions:
        print("No expenses found in " + category)
    total = sum(transaction[0] for transaction in transactions)
    return total

def select_transactions_by_date(start_date, end_date):
    connect = sqlite3.connect('Finance-Manager-Project\FinanceManager.db')
    cursor = connect.cursor()
    cursor.execute('''
    SELECT * FROM transactions WHERE date BETWEEN ? AND ?''', 
    (start_date, end_date))
    transactions = cursor.fetchall()
    connect.commit()
    connect.close()
    if not transactions:
        print("No expenses found between " + start_date + " and " + end_date)
    return transactions

def edit_transaction(id, new_amount, new_category):
    if new_amount <= 0:
        raise ValueError("Amount must be positive")
    else:
        connect = sqlite3.connect('Finance-Manager-Project\FinanceManager.db')
        cursor = connect.cursor()
        cursor.execute('''
        UPDATE transactions SET amount=?, category=?
        WHERE id=?''', (new_amount, new_category, id))
        connect.commit()
        connect.close()

