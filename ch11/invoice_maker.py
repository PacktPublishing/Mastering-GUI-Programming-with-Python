import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class InvoiceForm(qtw.QWidget):

    submitted = qtc.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QFormLayout())
        self.inputs = {}
        self.inputs['Customer Name'] = qtw.QLineEdit()
        self.inputs['Customer Address'] = qtw.QPlainTextEdit()
        self.inputs['Invoice Date'] = qtw.QDateEdit(
            date=qtc.QDate.currentDate(), calendarPopup=True)
        self.inputs['Days until Due'] = qtw.QSpinBox(
            minimum=0, maximum=60, value=30)
        for label, widget in self.inputs.items():
            self.layout().addRow(label, widget)

        self.line_items = qtw.QTableWidget(
            rowCount=10, columnCount=3)
        self.line_items.setHorizontalHeaderLabels(
            ['Job', 'Rate', 'Hours'])
        self.line_items.horizontalHeader().setSectionResizeMode(
            qtw.QHeaderView.Stretch)
        self.layout().addRow(self.line_items)
        for row in range(self.line_items.rowCount()):
            for col in range(self.line_items.columnCount()):
                if col > 0:
                    w = qtw.QSpinBox(minimum=0, maximum=300)
                    self.line_items.setCellWidget(row, col, w)
        submit = qtw.QPushButton('Create Invoice', clicked=self.on_submit)
        self.layout().addRow(submit)

    def on_submit(self):
        data = {
            'c_name': self.inputs['Customer Name'].text(),
            'c_addr': self.inputs['Customer Address'].toPlainText(),
            'i_date': self.inputs['Invoice Date'].date().toString(),
            'i_due': self.inputs['Invoice Date'].date().addDays(
                self.inputs['Days until Due'].value()).toString(),
            'i_terms': '{} days'.format(self.inputs['Days until Due'].value())
        }
        data['line_items'] = []
        for row in range(self.line_items.rowCount()):
            if not self.line_items.item(row, 0):
                continue
            job = self.line_items.item(row, 0).text()
            rate = self.line_items.cellWidget(row, 1).value()
            hours = self.line_items.cellWidget(row, 2).value()
            total = rate * hours
            row_data = [job, rate, hours, total]
            if any(row_data):
                data['line_items'].append(row_data)
        data['total_due'] = sum(x[3] for x in data['line_items'])
        self.submitted.emit(data)


class InvoiceView(qtw.QTextEdit):

    dpi = 72
    doc_width = 8.5 * dpi
    doc_height = 11 * dpi

    def __init__(self):
        super().__init__(readOnly=True)
        self.setFixedSize(qtc.QSize(self.doc_width, self.doc_height))


    def build_invoice(self, data):
        document = qtg.QTextDocument()
        self.setDocument(document)
        document.setPageSize(qtc.QSizeF(self.doc_width, self.doc_height))
        cursor = qtg.QTextCursor(document)
        root = document.rootFrame()
        cursor.setPosition(root.lastPosition())

        # Insert top-level frames
        logo_frame_fmt = qtg.QTextFrameFormat()
        logo_frame_fmt.setBorder(2)
        logo_frame_fmt.setPadding(10)
        logo_frame = cursor.insertFrame(logo_frame_fmt)

        cursor.setPosition(root.lastPosition())
        cust_addr_frame_fmt = qtg.QTextFrameFormat()
        cust_addr_frame_fmt.setWidth(self.doc_width * .3)
        cust_addr_frame_fmt.setPosition(qtg.QTextFrameFormat.FloatRight)
        cust_addr_frame = cursor.insertFrame(cust_addr_frame_fmt)

        cursor.setPosition(root.lastPosition())
        terms_frame_fmt = qtg.QTextFrameFormat()
        terms_frame_fmt.setWidth(self.doc_width * .5)
        terms_frame_fmt.setPosition(qtg.QTextFrameFormat.FloatLeft)
        terms_frame = cursor.insertFrame(terms_frame_fmt)

        cursor.setPosition(root.lastPosition())
        line_items_frame_fmt = qtg.QTextFrameFormat()
        line_items_frame_fmt.setMargin(25)
        line_items_frame = cursor.insertFrame(line_items_frame_fmt)

        # Create the heading
        # create a format for the characters
        std_format = qtg.QTextCharFormat()

        logo_format = qtg.QTextCharFormat()
        logo_format.setFont(
            qtg.QFont('Impact', 24, qtg.QFont.DemiBold))
        logo_format.setUnderlineStyle(
            qtg.QTextCharFormat.SingleUnderline)
        logo_format.setVerticalAlignment(
            qtg.QTextCharFormat.AlignMiddle)

        label_format = qtg.QTextCharFormat()
        label_format.setFont(qtg.QFont('Sans', 12, qtg.QFont.Bold))

        # create a format for the block
        cursor.setPosition(logo_frame.firstPosition())
        # The easy way:
        #cursor.insertImage('nc_logo.png')
        # The better way:
        logo_image_fmt = qtg.QTextImageFormat()
        logo_image_fmt.setName('nc_logo.png')
        logo_image_fmt.setHeight(48)
        cursor.insertImage(logo_image_fmt, qtg.QTextFrameFormat.FloatLeft)
        cursor.insertText('   ')
        cursor.insertText('Ninja Coders, LLC', logo_format)
        cursor.insertBlock()
        cursor.insertText('123 N Wizard St, Yonkers, NY 10701', std_format)

        ## Customer address
        cursor.setPosition(cust_addr_frame.lastPosition())

        address_format = qtg.QTextBlockFormat()
        address_format.setLineHeight(
            150, qtg.QTextBlockFormat.ProportionalHeight)
        address_format.setAlignment(qtc.Qt.AlignRight)
        address_format.setRightMargin(25)

        cursor.insertBlock(address_format)
        cursor.insertText('Customer:', label_format)
        cursor.insertBlock(address_format)
        cursor.insertText(data['c_name'], std_format)
        cursor.insertBlock(address_format)
        cursor.insertText(data['c_addr'])

        ## Terms
        cursor.setPosition(terms_frame.lastPosition())
        cursor.insertText('Terms:', label_format)
        cursor.insertList(qtg.QTextListFormat.ListDisc)
        # cursor is now in the first list item

        term_items = (
            f'<b>Invoice dated:</b> {data["i_date"]}',
            f'<b>Invoice terms:</b> {data["i_terms"]}',
            f'<b>Invoice due:</b> {data["i_due"]}',
        )

        for i, item in enumerate(term_items):
            if i > 0:
                cursor.insertBlock()
            # We can insert HTML too, but not with a textformat
            cursor.insertHtml(item)

        ## Line items
        table_format = qtg.QTextTableFormat()
        table_format.setHeaderRowCount(1)
        table_format.setWidth(
            qtg.QTextLength(qtg.QTextLength.PercentageLength, 100))

        headings = ('Job', 'Rate', 'Hours', 'Cost')
        num_rows = len(data['line_items']) + 1
        num_cols = len(headings)

        cursor.setPosition(line_items_frame.lastPosition())
        table = cursor.insertTable(num_rows, num_cols, table_format)

        # now we're in the first cell of the table
        # write headers
        for heading in headings:
            cursor.insertText(heading, label_format)
            cursor.movePosition(qtg.QTextCursor.NextCell)

        # write data
        for row in data['line_items']:
            for col, value in enumerate(row):
                text = f'${value}' if col in (1, 3) else f'{value}'
                cursor.insertText(text, std_format)
                cursor.movePosition(qtg.QTextCursor.NextCell)

        # Append a row
        table.appendRows(1)
        cursor = table.cellAt(num_rows, 0).lastCursorPosition()
        cursor.insertText('Total', label_format)
        cursor = table.cellAt(num_rows, 3).lastCursorPosition()
        cursor.insertText(f"${data['total_due']}", label_format)

        # Set the document




class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        # Main UI code goes here
        main = qtw.QWidget()
        main.setLayout(qtw.QHBoxLayout())
        self.setCentralWidget(main)

        form = InvoiceForm()
        main.layout().addWidget(form)

        self.preview = InvoiceView()
        main.layout().addWidget(self.preview)

        form.submitted.connect(self.preview.build_invoice)

        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
