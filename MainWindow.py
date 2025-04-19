import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow, QLineEdit
from methods import compute_entropy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.P_A_edit = QLineEdit("0.1, 0.12, 0.12, 0.15, 0.1, 0.15")
        self.P_B_edit = QLineEdit("0.25, 0.3, 0.01, 0.25, 0.025, 0.008, 0.0016, 0.0016")
        self.T_counts_edit = QLineEdit("256, 128, 256, 128, 132, 100, 200")
        self.P_joint_edit = QLineEdit("0,0.3,0;0.1,0,0.4;0.1,0,0")

        self.H_A_label = QLabel("", self)
        self.H_B_label = QLabel("", self)
        self.H_T_label = QLabel("", self)
        self.H_AB_label = QLabel("", self)
        self.H_A_given_B_label = QLabel("", self)
        self.H_B_given_A_label = QLabel("", self)

        self.calculate_H_A_B_pushbutton = QPushButton("Calculate #1", self)
        self.calculate_H_T_pushbutton = QPushButton("Calculate #2", self)
        self.calculate_H_AB_BA_pushbutton = QPushButton("Calculate #3", self)

        self.calculate_H_A_B_pushbutton.clicked.connect(self.set_h_a_b_label_text)
        self.calculate_H_T_pushbutton.clicked.connect(self.set_h_t_label_text)
        self.calculate_H_AB_BA_pushbutton.clicked.connect(self.set_h_AB_AtoB_BtoA_label_text)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('TIK Lab 2')
        self.setGeometry(1000, 200, 600, 600)
        self.setWindowIcon(QIcon('LAB2_icon.png'))

        qvbox = QVBoxLayout()
        qvbox.setSpacing(20)

        qvbox.addWidget(QLabel("P_A:"))
        qvbox.addWidget(self.P_A_edit)
        qvbox.addWidget(QLabel("P_B:"))
        qvbox.addWidget(self.P_B_edit)
        qvbox.addWidget(QLabel("T_counts:"))
        qvbox.addWidget(self.T_counts_edit)
        qvbox.addWidget(QLabel("P_joint (через ; строки, внутри через ,):"))
        qvbox.addWidget(self.P_joint_edit)

        qvbox.addWidget(self.H_A_label)
        qvbox.addWidget(self.H_B_label)
        qvbox.addWidget(self.calculate_H_A_B_pushbutton)
        qvbox.addWidget(self.H_T_label)
        qvbox.addWidget(self.calculate_H_T_pushbutton)
        qvbox.addWidget(self.H_AB_label)
        qvbox.addWidget(self.H_A_given_B_label)
        qvbox.addWidget(self.H_B_given_A_label)
        qvbox.addWidget(self.calculate_H_AB_BA_pushbutton)

        central_widget = QWidget()
        central_widget.setLayout(qvbox)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: rgb(255, 255, 255);
            }
            QLabel {
                background-color: transparent;
                font-family: Helvetica;
                font-size: 18px;
                font-weight: bold;
                color: rgb(0,0,0);
            }
            QPushButton {
                background-color: rgb(174, 201, 212);
                font-family: Helvetica;
                font-size: 18px;
                font-weight: bold;
                border: 3px solid;
                border-color: rgb(84, 129, 148);
                color: rgb(0,0,0);
                padding-left: 10px;
                width: 120px;
                height: 60px;
            }
            QLineEdit {
                background-color: rgb(240, 248, 250);
                font-family: Helvetica;
                font-size: 16px;
                border: 2px solid rgb(84, 129, 148);
                border-radius: 4px;
                padding: 6px;
                color: rgb(0,0,0);
            }
        """)

        self.show()

    def get_array_from_edit(self, edit, dtype=float):
        text = edit.text()
        parts = text.replace(" ", "").split(",")
        return np.array([dtype(p) for p in parts])

    def get_matrix_from_edit(self, edit):
        lines = edit.text().split(";")
        matrix = []
        for line in lines:
            row = [float(x) for x in line.replace(" ", "").split(",")]
            matrix.append(row)
        return np.array(matrix)

    def compute_H_A_and_H_B(self):
        P_A = self.get_array_from_edit(self.P_A_edit)
        P_B = self.get_array_from_edit(self.P_B_edit)
        H_A = compute_entropy(P_A)
        H_B = compute_entropy(P_B)
        return H_A, H_B

    def compute_H_T(self):
        T_counts = self.get_array_from_edit(self.T_counts_edit)
        P_T = T_counts / T_counts.sum()
        return compute_entropy(P_T)

    def compute_joint_entropy(self):
        P_joint = self.get_matrix_from_edit(self.P_joint_edit)
        P_A_marginal = np.sum(P_joint, axis=1)
        P_B_marginal = np.sum(P_joint, axis=0)
        H_AB = compute_entropy(P_joint[P_joint > 0])
        H_A_given_B = H_AB - compute_entropy(P_B_marginal[P_B_marginal > 0])
        H_B_given_A = H_AB - compute_entropy(P_A_marginal[P_A_marginal > 0])
        return H_AB, H_A_given_B, H_B_given_A

    def set_h_a_b_label_text(self):
        H_A, H_B = self.compute_H_A_and_H_B()
        self.H_A_label.setText(f"H_A = {H_A:.2f}")
        self.H_B_label.setText(f"H_B = {H_B:.2f}")
        self.set_default_text(self.H_A_label, "")
        self.set_default_text(self.H_B_label, "")

    def set_h_t_label_text(self):
        H_T = self.compute_H_T()
        self.H_T_label.setText(f"H_T = {H_T:.2f}")
        self.set_default_text(self.H_T_label, "")

    def set_h_AB_AtoB_BtoA_label_text(self):
        H_AB, H_A_given_B, H_B_given_A = self.compute_joint_entropy()
        self.H_AB_label.setText(f"H_AB = {H_AB:.2f}")
        self.H_A_given_B_label.setText(f"H_A_given_B = {H_A_given_B:.2f}")
        self.H_B_given_A_label.setText(f"H_B_given_A = {H_B_given_A:.2f}")
        self.set_default_text(self.H_AB_label, "")
        self.set_default_text(self.H_A_given_B_label, "")
        self.set_default_text(self.H_B_given_A_label, "")

    def set_default_text(self, button, text):
        QTimer.singleShot(10000, lambda: button.setText(text))
