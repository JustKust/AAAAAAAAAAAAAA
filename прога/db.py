import pymysql
import datetime

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='Cahrxisjy8252',
            database='cfcgdfgh',
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
        cursor.execute(
            f"INSERT INTO Shopping_list"
            f"(`Price`, `Amount`, `OrderID`, `ProductID`)"
            f"VALUES ('{price}', '{amount}', '{orderID}', '{ProductID}')"
        )
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

    def get_product_list(self):
        cur = self.connection.cursor()
        p_list = [str(i)[1:-2] for i in cur.execute("SELECT Name FROM Product")]
        cur.close()
        return p_list

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
        cursor.close()
        return id[1:-1]

if __name__ == '__main__':
    D = Database()