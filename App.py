import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QStringListModel
from mainwin import Ui_MainWindow 

class MyApp(QMainWindow):
    def __init__(self):

        # setup
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # yhdistää handleriin
        self.ui.pushButton.clicked.connect(self.handle_button_click)
        self.list_model = QStringListModel()
        self.ui.listView.setModel(self.list_model)

    def handle_button_click(self):
        text = self.ui.lineEdit.text()
        string_list = self.list_model.stringList()
        string_list.append(text)
        self.list_model.setStringList(string_list)
        print(text)

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()