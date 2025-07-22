from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db(db_name):
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(db_name)

    if not database.open():
        return False
    
    query = QSqlQuery()
    query.exec("""
               CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    description TEXT
               )
               """)
    
    return True

def fetch_expenses():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []
    while query.next():
        row = [query.value(i) for i in range(5)]
        expenses.append(row)
    return expenses

def add_expenses(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
                  INSERT INTO expenses (date, category, amount, description)
                  VALUES (?, ?, ?, ?)
                  """)
    
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    return query.exec()

def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id = ?")
    query.addBindValue(expense_id)
    return query.exec()

def fetch_date_expenses(date=None, month=None, year=None):
    query = QSqlQuery()

    if date:
        query.prepare("SELECT * FROM expenses WHERE date = :date ORDER BY date DESC")
        query.bindValue(":date", date)
    elif month:
        query.prepare("SELECT * FROM expenses WHERE date LIKE :month || '%' ORDER BY date DESC")
        query.bindValue(":month", month)
    elif year:
        query.prepare("SELECT * FROM expenses WHERE date LIKE :year || '%' ORDER BY date DESC")
        query.bindValue(":year", year)
    else:
        query.prepare("SELECT * FROM expenses ORDER BY date DESC")

    if not query.exec():
        print("Query failed:", query.lastError().text())
        return []

    expenses = []
    while query.next():
        row = [query.value(i) for i in range(5)]
        expenses.append(row)

    return expenses
