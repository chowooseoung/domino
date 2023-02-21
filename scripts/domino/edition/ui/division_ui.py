# gui
from PySide2 import QtWidgets


class DivisionUI(QtWidgets.QDialog):
    ui_name = "DominoDivisionUI"

    def __init__(self, parent=None):
        super(DivisionUI, self).__init__(parent=parent)
        self.number = 0
        self.setWindowTitle("Division Input")
        self.setObjectName(self.ui_name)

        self.create_widgets()
        self.create_connections()

    def create_widgets(self):
        layout = QtWidgets.QVBoxLayout(self)

        label = QtWidgets.QLabel("Number")
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setText("4")
        value_layout = QtWidgets.QHBoxLayout()
        value_layout.addWidget(label)
        value_layout.addWidget(self.line_edit)

        layout.addLayout(value_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("Ok")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def create_connections(self):
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
