import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            database='cfcgdfgh'
        )

    def getCLients(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM client")
        clients = cursor.fetchall()
        return clients

    def getEmployees(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM employee")
        employee = cursor.fetchall()
        cursor.close()
        return employee

    def getCompany(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM company")
        Company = cursor.fetchall()
        cursor.close()
        return Company

    def getProduct(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM product")
        product = cursor.fetchall()
        cursor.close()
        return product

    def getOrders(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        cursor.close()
        return orders

    def getProductList(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM shopping_list")
        ProductList = cursor.fetchall()
        cursor.close()
        return ProductList

    def insertOrder(self, post_index, country, city, street, client_name, client_code, emp_code):
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO Orders"
            f"(`post_index`, `country`, `city`, `street`, `Client_Name`, `ClientID`, `EmployeeID`)"
            f"VALUES ('{post_index}', '{country}', '{city}', '{street}', '{client_name}', '{client_code}', '{emp_code}')"
        )
        cursor.close()
        self.connection.commit()

    def insertProductInList(self, price, amount, orderID, ProductID):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Shopping_list VALUES (NULL, %s, %s, %s, %s)", (price, amount, orderID, ProductID))
        cursor.close()
        self.connection.commit()

    def insertProduct(self, name, cost, availability, CompID):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Product VALUES (NULL, %s, %s, %s, %s)", (name, cost, availability, CompID))
        cursor.close()
        self.connection.commit()

    def insertCompany(self, name, email, phone):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Company VALUES (NULL, %s, %s, %s)", (name, email, phone))
        cursor.close()
        self.connection.commit()

    def insertEmp(self, name, surname, post, phone, email, log, pas):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Employee VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)", (name, surname, post, phone, email, log, pas))
        cursor.close()
        self.connection.commit()

    def check_login(self):
        log = []
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT login FROM employee""")
        rows = cursor.fetchall()
        for i in rows:
            for j in i:
                log.append(j)
        cursor.close()
        return log

    def get_log(self, login):
        log = []
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT password, post FROM employee WHERE login = '{login}'""")
        rows = cursor.fetchall()
        for i in rows :
            for j in i:
                log.append(j)
        cursor.close()
        return log

    def get_orders_id(self):
        id_list = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT OrderID FROM Orders")
        rows = cursor.fetchall()
        for i in rows:
            id_list.append(str(i)[1:-2])
        cursor.close()
        return id_list

    def get_product_list(self):
        ProdList = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT Name FROM Product")
        rows = cursor.fetchall()
        for i in rows:
            ProdList.append(str(i)[2:-3])
        cursor.close()
        return ProdList

    def get_cost(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT Cost FROM Product WHERE Name = '{name}'""")
        cost = str(cursor.fetchone())
        cursor.close()
        return cost[1:-2]

    def get_product_id(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT ProductID FROM Product WHERE Name = '{name}'""")
        id = cursor.fetchone()
        for i in id:
            return i
        cursor.close()

    def get_comp_names(self):
        CompList = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT Name FROM Company")
        rows = cursor.fetchall()
        for i in rows:
            CompList.append(str(i)[2:-3])
        cursor.close()
        return CompList

    def get_comp_id(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT CompanyID FROM Company WHERE Name = '{name}'""")
        id = cursor.fetchone()
        for i in id:
            return i
        cursor.close()

    def get_client_id(self):
        id_list = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT ClientID FROM Client")
        rows = cursor.fetchall()
        for i in rows:
            id_list.append(str(i)[1:-2])
        cursor.close()
        return id_list

    def get_emp_id(self):
        id_list = []
        cursor = self.connection.cursor()
        cursor.execute("SELECT EmployeeID FROM Employee")
        rows = cursor.fetchall()
        for i in rows:
            id_list.append(str(i)[1:-2])
        cursor.close()
        return id_list

    def get_client_name(self, id):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT Name FROM Client WHERE ClientID = '{id}'""")
        cost = str(cursor.fetchone())
        cursor.close()
        return cost[2:-3]

if __name__ == '__main__':
    D = Database()
