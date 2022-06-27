import sys
from db import Database
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog, QTableWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("forms/admin.ui", self)
        self.setWindowTitle("ничто")


    def authoriz(self, wnd):
        dialog = DialogAutorization(wnd)
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()

class DialogAutorization(QDialog):
    def __init__(self, wnd, parent = None):
        self.wnd = wnd
        super(DialogAutorization, self).__init__(parent)
        self.ui = uic.loadUi("forms/auth.ui", self)
        self.setWindowTitle("Авторизация?")
        self.ui.autorization_btn.clicked.connect(self.autoriz)
        self.db = Database()

    def autoriz(self):
        login = self.ui.line_log.text()
        password = self.ui.line_pas.text()

        if login == '' or password == '':
            self.empty_pole()
        elif login not in self.db.check_login():
            self.wrong_log_msg()
        else:
            aut = self.db.get_log(login)
            autpas = aut[0]
            role = aut[1]
            if password != autpas:
                self.wrong_pass_msg()
            else:
                if role == 'Администратор':
                    self.admin_open()
                if role == 'Продавец':
                    self.seller_open()

    def admin_open(self):
        self.ui.close()
        self.ui = AdminMenu()
        self.ui.show()

    def seller_open(self):
        self.ui.close()
        self.ui = SellerMenu()
        self.ui.show()

    def empty_pole(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Заполните все необходимые поля!")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

    def wrong_pass_msg(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Неверно введен пароль!")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

    def wrong_log_msg(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка ввода")
        self.mesbox.setText("Неверно введен логин.")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

class AdminMenu(QMainWindow):
    def __init__(self):
        super(AdminMenu, self).__init__()
        self.ui = uic.loadUi("forms/admin.ui", self)
        self.window().setWindowTitle("Admin")
        self.db = Database()
        self.ui.emp_btn.clicked.connect(self.employee)
        self.ui.product_btn.clicked.connect(self.product)
        self.ui.comp_btn.clicked.connect(self.company)
        self.ui.back_btn.clicked.connect(self.exit)
        self.table = self.ui.tableWidget
        self.employee()

    def employee(self):
        self.table.clear()
        out = self.db.getEmployees()
        self.table.setColumnCount(8)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'Имя', 'Фамилия', 'Должность', 'Телефон', 'Почта', 'Логин', 'Пароль'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def product(self):
        self.table.clear()
        out = self.db.getProduct()
        self.table.setColumnCount(5)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Цена', 'Количество', 'ID компании'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def company(self):
        self.table.clear()
        out = self.db.getCompany()
        self.table.setColumnCount(4)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Почта', 'Номер'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def exit(self):
        dialog = DialogAutorization(self.window)
        self.ui.close()
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()

class SellerMenu(QMainWindow):
    def __init__(self):
        super(SellerMenu, self).__init__()
        self.ui = uic.loadUi("forms/seller.ui", self)
        self.window().setWindowTitle("Seller")
        self.table = self.ui.order_table
        self.db = Database()
        self.ui.order_add_btn.clicked.connect(self.add_order)
        self.ui.add_product_btn.clicked.connect(self.add_product)
        self.ui.product_list_btn.clicked.connect(self.product_list)
        self.ui.order_list.clicked.connect(self.orders)
        self.table = self.ui.order_table
        self.ui.back_btn.clicked.connect(self.exit)
        self.orders()

    def exit(self):
        dialog = DialogAutorization(self.window)
        self.ui.close()
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()

    def orders(self):
        self.table.clear()
        out = self.db.getOrders()
        self.table.setColumnCount(8)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'Индекс', 'Страна','Город','Улица','Имя клиента','Код клиента', 'Код сотрудника'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def product_list(self):
        self.table.clear()
        out = self.db.getProductList()
        self.table.setColumnCount(5)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Цена', 'Количество', 'Код заказа', 'Код товара'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                if x == 0:  # для id делаем некликабельные ячейки
                    item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def add_order(self):
        dialog = DialogAdd()
        dialog.setWindowTitle("Добавить заказ")
        dialog.show()
        dialog.exec_()

    def add_product(self):
        dialog = DialogAddProduct()
        dialog.setWindowTitle("Добавить продукт")
        dialog.show()
        dialog.exec_()

class DialogAdd(QDialog):
    def __init__(self):
        super(DialogAdd, self).__init__()
        self.ui = uic.loadUi("forms/dialog_add_order.ui", self)
        self.setWindowTitle("Добавить заказ")
        self.db = Database()
        self.ui.add_btn_2.clicked.connect(self.add_order)

    def add_order(self):
        post_index = self.ui.post_index.text()
        country = self.ui.country.text()
        city = self.ui.city.text()
        street = self.ui.street.text()
        client_name = self.ui.client_name.text()
        client_code = self.ui.client_code.text()
        emp_code = self.ui.emp_code.text()
        self.db.insertOrder(post_index, country, city, street, client_name, client_code, emp_code)
        self.ui.close()

class DialogAddProduct(QDialog):
    def __init__(self):
        super(DialogAddProduct, self).__init__()
        self.ui = uic.loadUi("forms/add_product.ui", self)
        self.setWindowTitle("Добавить товар")
        self.db = Database()
        self.ui.add_btn.clicked.connect(self.add_product)
        self.ui.close_btn.clicked.connect(self.ui.close)

    def add_product(self):
        amount = int(self.ui.amount.text())
        orderid = int(self.ui.order_code.text())
        name = self.ui.product.text()
        cost = int(self.db.get_cost(name))
        productid = int(self.db.get_product_id(name))
        full_cost = amount*cost
        self.db.insertProductInList(full_cost, amount, orderid, productid)

class Builder:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.wnd = MainWindow()
        self.auth()

    def auth(self):
        self.wnd.authoriz(self.wnd)
        self.app.exec()

if __name__ == '__main__':
    B = Builder()