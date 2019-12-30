import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtSql as qts


class CoffeeForm(qtw.QWidget):
    """Form to display/edit all info about a coffee"""

    def __init__(self, roasts):
        super().__init__()
        self.setLayout(qtw.QFormLayout())

        self.coffee_brand = qtw.QLineEdit()
        self.layout().addRow('Brand: ', self.coffee_brand)
        self.coffee_name = qtw.QLineEdit()
        self.layout().addRow('Name: ', self.coffee_name)
        self.roast = qtw.QComboBox()
        self.roast.addItems(roasts)
        self.layout().addRow('Roast: ', self.roast)
        self.reviews = qtw.QTableWidget(columnCount=3)
        self.reviews.horizontalHeader().setSectionResizeMode(
            2, qtw.QHeaderView.Stretch)
        self.layout().addRow(self.reviews)

    def show_coffee(self, coffee_data, reviews):
        self.coffee_brand.setText(coffee_data.get('coffee_brand'))
        self.coffee_name.setText(coffee_data.get('coffee_name'))
        self.roast.setCurrentIndex(coffee_data.get('roast_id'))
        self.reviews.clear()
        self.reviews.setHorizontalHeaderLabels(
            ['Reviewer', 'Date', 'Review'])
        self.reviews.setRowCount(len(reviews))
        for i, review in enumerate(reviews):
            for j, value in enumerate(review):
                self.reviews.setItem(i, j, qtw.QTableWidgetItem(value))


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        Code in this method should define window properties,
        create backend resources, etc.
        """
        super().__init__()
        # Code starts here
        self.stack = qtw.QStackedWidget()
        self.setCentralWidget(self.stack)

        # Connect to the database
        self.db = qts.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('coffee.db')
        if not self.db.open():
            error = self.db.lastError().text()
            qtw.QMessageBox.critical(
                None, 'DB Connection Error',
                'Could not open database file: '
                f'{error}')
            sys.exit(1)

        # Check for missing tables
        required_tables = {'roasts', 'coffees', 'reviews'}
        tables = self.db.tables()
        missing_tables = required_tables - set(tables)
        if missing_tables:
            qtw.QMessageBox.critical(
                None, 'DB Integrity Error',
                'Missing tables, please repair DB: '
                f'{missing_tables}')
            sys.exit(1)

        # Make a query
        query = self.db.exec('SELECT count(*) FROM coffees')
        query.next()
        count = query.value(0)
        print(f'There are {count} coffees in the database.')

        # Retreive the roasts table
        query = self.db.exec('SELECT * FROM roasts ORDER BY id')
        roasts = []
        while query.next():
            roasts.append(query.value(1))

        # create the form
        self.coffee_form = CoffeeForm(roasts)
        self.stack.addWidget(self.coffee_form)

        # Retreive the coffees table using a QSqlQueryModel
        coffees = qts.QSqlQueryModel()
        coffees.setQuery(
            "SELECT id, coffee_brand, coffee_name AS coffee "
            "FROM coffees ORDER BY id")
        self.coffee_list = qtw.QTableView()
        self.coffee_list.setModel(coffees)
        self.stack.addWidget(self.coffee_list)
        self.stack.setCurrentWidget(self.coffee_list)

        coffees.setHeaderData(1, qtc.Qt.Horizontal, 'Brand')
        coffees.setHeaderData(2, qtc.Qt.Horizontal, 'Product')

        # Navigation between stacked widgets
        navigation = self.addToolBar("Navigation")
        navigation.addAction(
            "Back to list",
            lambda: self.stack.setCurrentWidget(self.coffee_list))

        self.coffee_list.doubleClicked.connect(
            lambda x: self.show_coffee(self.get_id_for_row(x)))

        # Code ends here
        self.show()

    def get_id_for_row(self, index):
        index = index.siblingAtColumn(0)
        coffee_id = self.coffee_list.model().data(index)
        return coffee_id

    def show_coffee(self, coffee_id):
        # get the basic coffee information
        query1 = qts.QSqlQuery(self.db)
        query1.prepare('SELECT * FROM coffees WHERE id=:id')
        query1.bindValue(':id', coffee_id)
        query1.exec()
        query1.next()
        coffee = {
            'id': query1.value(0),
            'coffee_brand': query1.value(1),
            'coffee_name': query1.value(2),
            'roast_id': query1.value(3)
        }
        # get the reviews
        query2 = qts.QSqlQuery()
        query2.prepare('SELECT * FROM reviews WHERE coffee_id=:id')
        query2.bindValue(':id', coffee_id)
        query2.exec()
        reviews = []
        while query2.next():
            reviews.append((
                query2.value('reviewer'),
                query2.value('review_date'),
                query2.value('review')
            ))

        self.coffee_form.show_coffee(coffee, reviews)
        self.stack.setCurrentWidget(self.coffee_form)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
