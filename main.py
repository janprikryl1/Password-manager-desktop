from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QIcon
import sys
import sqlite3
import os



'''app2 = QtWidgets.QApplication([])
w2 = QtWidgets.QMainWindow()
class ADD(QWidget):

    def __init__(self, id):
        super().__init__()
        with open('add.ui') as f2:
            uic.loadUi(f2, w2)
        w2.pushButton.clicked.connect(lambda: Main.save(Main, id, w2.lineEdit.text(), w2.lineEdit_2.text(), w2.lineEdit_3.text()))
        w2.show()
        #♦return w2.lineEdit.text()'''
    

app = QtWidgets.QApplication([])
window = QtWidgets.QMainWindow()
class Main(QWidget):
    def __init__(self):
        super().__init__()
        with open('main.ui') as f:
            uic.loadUi(f, window)
        self.status_label = QtWidgets.QLabel(window)
        window.statusbar.addWidget(self.status_label)
        window.setWindowTitle("Správce hesel")  
#        self.item_list = window.verticalLayout
        window.actionAdd.triggered.connect(self.add_user)
        window.actionNov_p_ihl_en.triggered.connect(self.new_sign)
        window.actionP_idat.triggered.connect(self.add_item_show)


        if not os.path.isfile('data.db'):
            self.database = sqlite3.connect('data.db')
            self.d = self.database.cursor()
            self.d.execute("CREATE TABLE USERS(id INTEGER PRIMARY KEY, name VARCHAR(25), password VARCHAR(25));")
            self.d.execute("CREATE TABLE item(id INTEGET PRIMARY KEY, title VARCHAR(30), password VARCHAR(45), user INTEGER, web VARCHAR(45), FOREIGN KEY(user) REFERENCES USER(id));")
            name = self.getText("Vaše jméno:")
            password  = self.getPassword(f"Vytvoření uživatele {name}", "Heslo:")
            self.d.execute(f'INSERT INTO USERS VALUES(1, "{name}", "{password}");')
            self.database.commit()
            self.login()
        else:
            self.database = sqlite3.connect('data.db')
            self.d = self.database.cursor()
            self.login()

                
        window.show()
        return app.exec()

    def login(self):
        items = []
        for i in self.d.execute("SELECT name FROM USERS;"):
            items.append(i[0])
        self.username, okPressed = QInputDialog.getItem(self, "Vyberte uživatele","Uživatel:", items, 0, False)
        self.password = self.getPassword("Zadejte heslo", self.username)
        if self.d.execute(f'SELECT password FROM USERS WHERE name = "{self.username}"').fetchone()[0] == self.password:
            self.id = self.d.execute(f'SELECT id FROM USERS WHERE name = "{self.username}" AND password = "{self.password}";').fetchone()[0]
            
            self.status_label.setText("Uživatel: " + self.username)
            
            self.load()
        else:
            buttonReply = QMessageBox.question(self, 'Špatné heslo', "Ukončit aplikaci?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.close()
            else:
                self.login()


    def load(self):
        self.clearLayout(window.verticalLayout_2)
        for e in self.d.execute(f'SELECT * FROM item WHERE user = {self.id}'):
            
            label = QtWidgets.QLabel(window)
            label.setText(f'Web: {e[4]}, uživatel: {e[1]}, heslo: {e[2]}')
            button = QPushButton(str(e[4]), self)

            window.verticalLayout_2.addWidget(label)
            window.verticalLayout_2.addWidget(button)

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            item.widget().close()
            # remove the item from layout
            layout.removeItem(item)  


    def add_item_show(self):
        #ADD().save(self.user)
        #ADD(self.id)
        web = self.getText('Název webu')
        name = self.getText('Uživatelské jméno')
        password = self.getPassword(f'Heslo k webu {web}', name)
        _id = 1
        for i in self.d.execute('SELECT id FROM item'):
            _id = i
        _id = int(_id[0])+1
        self.d.execute(f'BEGIN;')
        self.d.execute(f'INSERT INTO item values({_id}, "{name}", "{password}", {self.id}, "{web}");')
        self.d.execute(f'COMMIT;')
        self.database.commit()
        self.load()

    def new_sign(self):
        self.username = None
        self.password = None
        self.id = None
        self.login()

    def add_user(self):
        name = self.getText("Jméno")
        if name:
            password = self.getPassword("Heslo", name)
            if password:
                i = self.d.execute('SELECT id FROM USERS').fetchone()
                i = int(i[len(i)-1])+1
                self.d.execute(f'INSERT INTO USERS values({i}, "{name}", "{password}");')
                self.database.commit()
                    
    def getText(self, title):
        text, okPressed = QInputDialog.getText(self, "Vytvoření profilu",title, QLineEdit.Normal, "")
        if okPressed:
            return text

    def getPassword(self, title, text):
        text, okPressed = QInputDialog.getText(self, title, text, QLineEdit.Password, "")
        if okPressed:
            return text

    def close(self):
        self.database.close()
        sys.exit(0)
    

main = Main()

