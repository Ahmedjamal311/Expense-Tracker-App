from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView, QSpinBox, QCheckBox

from PyQt6.QtCore import QDate
from database import fetch_expenses, add_expenses, delete_expenses, fetch_date_expenses

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()
        self.apply_filters()
    
    def settings(self):
        self.setGeometry(750, 300, 550, 500)
        self.setWindowTitle("Financial Manager App")
    
    def initUI(self):
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton("Add Expense")
        self.btn_delete = QPushButton("Remove Expense")

        self.table = QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_dropdown()

        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense)

        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItem("All Categories")
        self.filter_dropdown.addItems(["Food", "Rent", "Bills", "Entertainment", "Shopping", "Other"])
        self.filter_dropdown.currentTextChanged.connect(self.apply_filters)

        self.date_filter = QDateEdit()
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.dateChanged.connect(self.apply_filters)

        self.enable_date_filter = QCheckBox("Use Exact Date")
        self.enable_date_filter.setChecked(False)
        self.enable_date_filter.stateChanged.connect(self.apply_filters)

        self.month_filter = QComboBox()
        self.month_filter.addItem("All Months")
        self.month_filter.addItems(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        self.month_filter.currentTextChanged.connect(self.apply_filters)

        self.year_filter = QSpinBox()
        self.year_filter.setRange(2000, QDate.currentDate().year() + 10)
        self.year_filter.setValue(QDate.currentDate().year())
        self.year_filter.valueChanged.connect(self.apply_filters)

        self.total_label = QLabel("Total Spent: $0.00")
        self.total_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.setup_layout()
        self.show()

    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)
        row1.addWidget(QLabel("Amount"))
        row1.addWidget(self.amount)
        row1.addWidget(QLabel("Description"))
        row1.addWidget(self.description)

        row2.addWidget(self.btn_add)
        row2.addWidget(self.btn_delete)
        
        row3.addWidget(QLabel("Filter Category:"))
        row3.addWidget(self.filter_dropdown)
        row3.addWidget(self.enable_date_filter)
        row3.addWidget(QLabel("Filter Date:"))
        row3.addWidget(self.date_filter)
        row3.addWidget(QLabel("Filter Month:"))
        row3.addWidget(self.month_filter)
        row3.addWidget(QLabel("Filter Year:"))
        row3.addWidget(self.year_filter)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()
        master.addLayout(total_layout)

        self.setLayout(master)

    def populate_dropdown(self):
        categories = ["Food", "Rent", "Bills", "Entertainment", "Shopping", "Other"]
        self.dropdown.addItems(categories)
    
    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for row_idx, expense in enumerate(expenses):
                self.table.insertRow(row_idx)
                for col_idx, data in enumerate(expense):
                    if col_idx == 3:
                        try:
                            amount = float(data)
                            if amount.is_integer():
                                formatted = f"${int(amount)}"
                            else:
                                formatted = f"${amount:.2f}"
                        except:
                            formatted = str(data)
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(formatted))
                    else:
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description can't be empty")
            return
        
        if add_expenses(date, category, amount, description):
            self.load_table_data()
            self.apply_filters()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "Failed to add expense")

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uh oh", "You need to choose a row to delete")
            return
        
        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):
            self.load_table_data()
            self.apply_filters()
    
    def calculate_total(self, expenses):
        total = 0.0
        for expense in expenses:
            try:
                total += float(expense[3])
            except (ValueError, IndexError):
                continue
        return total
    
    def apply_filters(self):
        selected_category = self.filter_dropdown.currentText()
        selected_month_name = self.month_filter.currentText()
        selected_year = self.year_filter.value()

        category_filter = selected_category if selected_category != "All Categories" else None

        if self.enable_date_filter.isChecked():
            date_filter = self.date_filter.date().toString("yyyy-MM-dd")
        else:
            date_filter = None

        month_filter = None
        year_filter = None

        if selected_month_name != "All Months":
            month_map = {
                "January": "01", "February": "02", "March": "03", "April": "04",
                "May": "05", "June": "06", "July": "07", "August": "08",
                "September": "09", "October": "10", "November": "11", "December": "12"
            }
            month_filter = f"{selected_year}-{month_map[selected_month_name]}"
        else:
            year_filter = str(selected_year)

        if date_filter:
            expenses = fetch_date_expenses(date=date_filter)
        elif month_filter:
            expenses = fetch_date_expenses(month=month_filter)
        elif year_filter:
            expenses = fetch_date_expenses(year=year_filter)
        else:
            expenses = fetch_expenses()

        if category_filter:
            expenses = [e for e in expenses if e[2] == category_filter]

        self.table.setRowCount(0)
        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                if col_idx == 3:
                    try:
                        amount = float(data)
                        if amount.is_integer():
                            formatted = f"${int(amount)}"
                        else:
                            formatted = f"${amount:.2f}"
                    except:
                        formatted = str(data)
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(formatted))
                else:
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

        total = self.calculate_total(expenses)
        if total.is_integer():
            self.total_label.setText(f"Total Spent: ${int(total)}")
        else:
            self.total_label.setText(f"Total Spent: ${total:.2f}")
