import app.chanda as chanda
import app.compare as compare
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox
from app.gui.mainwindow import Ui_MainWindow


class myWindow(QMainWindow):
    def __init__(self, app):
        super(myWindow, self).__init__()
        self.app = app
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.filename = ''
        self.connect_function()

    def connect_function(self):
        self.ui.actionCheck.triggered.connect(self.kabita_check)
        self.ui.actionOpen.triggered.connect(self.load_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSaveAs.triggered.connect(self.saveas_file)
        self.ui.actionNew.triggered.connect(self.new_file)
        self.ui.actionFromThisFile.triggered.connect(self.add_rule_from_file)
        self.ui.actionAutomaticDetect.triggered.connect(self.add_chanda_auto)
        self.ui.actionFromList.triggered.connect(self.add_chanda_from_list)

    def kabita_check(self):
        kabita = self.ui.MainInput.toPlainText()
        html = compare.analysis(kabita.split('\n'))
        self.ui.AnalysisOutput.setHtml(html)

    def new_file(self):
        self.ui.MainInput.setText('')
        self.filename = ''

    def load_file(self):
        file = QFileDialog.getOpenFileName()
        if file[0] == '':
            return
        self.filename = file[0]
        with open(file[0], 'r') as r:
            content = r.read()
        self.ui.MainInput.setText(content)

    def saveas_file(self):
        self.save_file(saveas=True)

    def save_file(self, saveas=False):
        if self.filename == '' or saveas:
            file = QFileDialog.getSaveFileName()
            if file[0] == '':
                return
            self.filename = file[0]
        with open(self.filename, 'w') as w:
            w.write(self.ui.MainInput.toPlainText())

    def add_chanda_auto(self):
        rule = compare.extract_chanda_rule(
            self.ui.MainInput.toPlainText().split('\n'))
        if rule == '':
            pass
        else:
            name = chanda.get_chanda_name(rule, '')
            content = self.ui.MainInput.toPlainText()
            if name == '':
                self.ui.MainInput.setText(f'# {rule}\n{content}')
            else:
                self.ui.MainInput.setText(
                    f'# {name}-छन्द-कविता\n# {rule}\n{content}')

    def add_rule_from_file(self):
        rule = compare.extract_chanda_rule(
            self.ui.MainInput.toPlainText().split('\n'))
        if rule == '':
            QMessageBox(QMessageBox.Critical, 'Error',
                        "Chanda Rule couldn't be detected").open()
        else:
            name = chanda.get_chanda_name(rule, '')
            content = self.ui.MainInput.toPlainText()
            if name == '':
                name = QInputDialog.getText(self, 'Input', 'Enter Chanda Name')
                if name[0] == '' or name[1] == False:
                    return
                chanda.add_chanda_rule(name[0], rule)
                self.ui.MainInput.setText(
                    f'# {name}-छन्द-कविता\n# {rule}\n{content}')
            else:
                QMessageBox(QMessageBox.Warning, 'Can not Add',
                            f'this rule is already in file stored as {name}.')

    def add_chanda_from_list(self):
        rules = chanda.get_chanda_list()
        name = QInputDialog.getItem(self, 'Add Chanda', 'Choose Chanda',
                                    [f'{n}-{r}' for r, n in rules.items()])
        if name[1]:
            content = self.ui.MainInput.toPlainText()
            name = name[0].split('-')
            rule = name[-1]
            name = name[0]
            self.ui.MainInput.setText(
                f'# {name}-छन्द-कविता\n# {rule}\n{content}')


if __name__ == '__main__':
    ui_app = QApplication([])
    ui_win = myWindow(ui_app)
    ui_win.show()
    ui_app.exec_()
