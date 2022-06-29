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
            self.mes_box('Заполните все поля!')
        elif login not in self.db.check_login():
            self.mes_box('Неверно введен логин!')
        else:
            aut = self.db.get_log(login)
            autpas = aut[0]
            role = aut[1]
            if password != autpas:
                self.mes_box('Неверно введен пароль!')
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

    def mes_box(self, text):
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

class AdminMenu(QMainWindow):
    def __init__(self):
        super(AdminMenu, self).__init__()
        self.ui = uic.loadUi("forms/admin.ui", self)
        self.window().setWindowTitle("Admin")
        self.db = Database()
        self.ui.emp_btn.clicked.connect(self.updateEmployee)
        self.ui.add_emp_btn.clicked.connect(self.add_emp)
        self.ui.product_btn.clicked.connect(self.updateProduct)
        self.ui.add_product_btn.clicked.connect(self.add_prod)
        self.ui.comp_btn.clicked.connect(self.updateCompany)
        self.ui.add_comp_btn.clicked.connect(self.add_comp)
        self.ui.back_btn.clicked.connect(self.exit)
        self.table = self.ui.tableWidget
        self.updateEmployee()

    def updateEmployee(self):
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

    def updateProduct(self):
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

    def updateCompany(self):
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

    def add_emp(self):
        dialog = DialogAddEmp()
        dialog.setWindowTitle("Добавить сотрудника")
        dialog.show()
        dialog.exec_()

    def add_prod(self):
        dialog = DialogAddProd(self)
        dialog.setWindowTitle("Добавить продукт")
        dialog.show()
        dialog.exec_()

    def add_comp(self):
        dialog = DialogAddCompany()
        dialog.setWindowTitle("Добавить компанию")
        dialog.show()
        dialog.exec_()

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
        dialog = DialogAddOrder()
        dialog.setWindowTitle("Добавить заказ")
        dialog.show()
        dialog.exec_()

    def add_product(self):
        dialog = DialogAddProduct()
        dialog.setWindowTitle("Добавить продукт")
        dialog.show()
        dialog.exec_()

class DialogAddOrder(QDialog):
    def __init__(self):
        super(DialogAddOrder, self).__init__()
        self.ui = uic.loadUi("forms/dialog_add_order.ui", self)
        self.setWindowTitle("Добавить заказ")
        self.db = Database()
        self.client_code.addItems(self.db.get_client_id())
        self.emp_code.addItems(self.db.get_emp_id())
        self.ui.add_btn_2.clicked.connect(self.add_order)
        self.ui.back_btn.clicked.connect(self.ui.close)

    def add_order(self):
        post_index = self.ui.post_index.text()
        country = self.ui.country.text()
        city = self.ui.city.text()
        street = self.ui.street.text()
        client_code = self.client_code.currentText()
        emp_code = self.emp_code.currentText()
        if post_index !='' and country !='' and city !='' and street !='' and client_code !='' and emp_code !='':
            client_name = self.db.get_client_name(client_code)
            self.db.insertOrder(post_index, country, city, street, client_name, int(client_code), int(emp_code))
            self.ui.close()
        else:
            self.mes_box('Заполните все поля')

    def mes_box(self, text):
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

class DialogAddProduct(QDialog):
    def __init__(self):
        super(DialogAddProduct, self).__init__()
        self.ui = uic.loadUi("forms/add_product.ui", self)
        self.setWindowTitle("Добавить товар")
        self.db = Database()
        prNames = self.db.get_product_list()
        orderId = self.db.get_orders_id()
        self.order_code.addItems(orderId)
        self.product.addItems(prNames)
        self.ui.add_btn.clicked.connect(self.add_product)
        self.ui.close_btn.clicked.connect(self.ui.close)

    def add_product(self):
        amount = self.ui.amount.text()
        orderid = self.order_code.currentText()
        name = self.product.currentText()
        if amount !='' and orderid !='' and name !='':
            cost = self.db.get_cost(name)
            productid = self.db.get_product_id(name)
            full_cost = amount * cost
            self.db.insertProductInList(int(full_cost), int(amount), int(orderid), int(productid))
        else:
            self.mes_box('Заполните все поля')

    def mes_box(self, text):
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

class DialogAddEmp(QDialog):
    def __init__(self):
        super(DialogAddEmp, self).__init__()
        self.ui = uic.loadUi("forms/add_emp.ui", self)
        self.setWindowTitle("Добавить заказ")
        self.db = Database()
        post = ['Администратор', 'Продавец']
        self.post_line.addItems(post)
        self.ui.add_btn.clicked.connect(self.add_emp)
        self.ui.close_btn.clicked.connect(self.ui.close)

    def add_emp(self):
        name = self.ui.name_line.text()
        surname = self.ui.surname_line.text()
        post = self.ui.post_line.text()
        phone = self.ui.phone_line.text()
        mail = self.ui.mail_line.text()
        log = self.ui.log_line.text()
        pas = self.ui.pass_line.text()
        if name !='' and surname !='' and post !='' and phone !='' and mail !='' and log !='' and pas != '':
            self.db.insertEmp(name, surname, post, phone, mail, log, pas)
            self.ui.close()
        else:
            self.mes_box('Заполните все поля')

    def mes_box(self, text):
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

class DialogAddCompany(QDialog):
    def __init__(self):
        super(DialogAddCompany, self).__init__()
        self.ui = uic.loadUi("forms/add_comp.ui", self)
        self.setWindowTitle("Добавить заказ")
        self.db = Database()
        self.ui.btn_add.clicked.connect(self.add_comp)
        self.ui.btn_close.clicked.connect(self.ui.close)

    def add_comp(self):
        name = self.ui.line_name.text()
        phone = self.ui.line_phone.text()
        mail = self.ui.line_mail.text()
        if name !='' and mail !='' and phone!='':
            self.db.insertCompany(name, mail, phone)
            self.ui.close()
        else:
            self.mes_box('Заполните все поля')

    def mes_box(self, text):
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

class DialogAddProd(QDialog):
    def __init__(self, parent=None):
        super(DialogAddProd, self).__init__(parent)
        self.ui = uic.loadUi("forms/add_prod.ui", self)
        self.setWindowTitle("Добавить заказ")
        self.db = Database()
        comp_names = self.db.get_comp_names()
        self.comp_line.addItems(comp_names)
        self.ui.btn_add.clicked.connect(self.add_prod)
        self.ui.btn_close.clicked.connect(self.ui.close)

    def add_prod(self):
        name = self.ui.line_name.text()
        cost = self.ui.cost_line.text()
        av = self.ui.av_line.text()
        comp = self.comp_line.currentText()
        comp = self.db.get_comp_id(comp)
        if name =='' or cost == '' or av =='' or comp =='':
            self.mes_box('Заполните все поля!')
        else:
            self.db.insertProduct(name, int(cost), int(av), int(comp))
            self.parent().updateProduct()
            self.ui.close()

    def mes_box(self, text):
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

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