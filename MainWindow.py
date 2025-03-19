import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMainWindow
from methods import compute_entropy


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.P_A = np.array([0.1, 0.12, 0.12, 0.15, 0.1, 0.15])
        self.P_B = np.array([0.25, 0.3, 0.01, 0.25, 0.025, 0.008, 0.0016, 0.0016])
        self.T_counts = np.array([256, 128, 256, 128, 132, 100, 200])
        self.P_joint = np.array([
            [0, 0.3, 0],
            [0.1, 0, 0.4],
            [0.1, 0, 0]
        ])

        # Else
        self.P_A_label = QLabel("P_A =", self)
        self.P_B_label = QLabel("P_B =", self)
        self.T_counts_label = QLabel("T_counts =", self)
        self.P_joint_label = QLabel("P_joint =", self)

        self.H_A_label = QLabel("", self)
        self.H_B_label = QLabel("", self)
        self.H_T_label = QLabel("", self)
        self.H_AB_label = QLabel("", self)
        self.H_A_given_B_label = QLabel("", self)
        self.H_B_given_A_label = QLabel("", self)

        # Push Buttons and their connections
        self.calculate_H_A_B_pushbutton = QPushButton("Calculate #1", self)
        self.calculate_H_T_pushbutton = QPushButton("Calculate #2", self)
        self.calculate_H_AB_BA_pushbutton = QPushButton("Calculate #3", self)

        self.calculate_H_A_B_pushbutton.clicked.connect(self.set_h_a_b_label_text)
        self.calculate_H_T_pushbutton.clicked.connect(self.set_h_t_label_text)
        self.calculate_H_AB_BA_pushbutton.clicked.connect(self.set_h_AB_AtoB_BtoA_label_text)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('TIK Lab 2')
        self.setGeometry(1000, 200, 600, 500)
        self.setWindowIcon(QIcon('LAB2_icon.png'))

        formatted_P_A = np.array2string(self.P_A, precision=3, separator=', ')
        formatted_P_B = np.array2string(self.P_B, precision=3, separator=', ')
        formatted_T_counts = np.array2string(self.T_counts, precision=3, separator=', ')

        self.P_A_label.setText(f"P_A = {formatted_P_A}")
        self.P_B_label.setText(f"P_B = {formatted_P_B}")
        self.T_counts_label.setText(f"T_counts = {formatted_T_counts}")

        self.P_A_label.setFixedHeight(50)
        self.P_B_label.setFixedHeight(50)
        self.T_counts_label.setFixedHeight(50)
        self.P_joint_label.setFixedHeight(100)
        self.H_A_label.setFixedHeight(50)
        self.H_B_label.setFixedHeight(50)
        self.H_T_label.setFixedHeight(50)
        self.H_AB_label.setFixedHeight(50)
        self.H_A_given_B_label.setFixedHeight(50)
        self.H_B_given_A_label.setFixedHeight(50)

        # Layout
        qvbox = QVBoxLayout()
        qvbox.setSpacing(20)

        qvbox.addWidget(self.P_A_label)
        qvbox.addWidget(self.P_B_label)
        qvbox.addWidget(self.H_A_label)
        qvbox.addWidget(self.H_B_label)
        qvbox.addWidget(self.calculate_H_A_B_pushbutton)
        qvbox.addWidget(self.T_counts_label)
        qvbox.addWidget(self.H_T_label)
        qvbox.addWidget(self.calculate_H_T_pushbutton)
        qvbox.addWidget(self.P_joint_label)
        qvbox.addWidget(self.H_AB_label)
        qvbox.addWidget(self.H_A_given_B_label)
        qvbox.addWidget(self.H_B_given_A_label)
        qvbox.addWidget(self.calculate_H_AB_BA_pushbutton)

        central_widget = QWidget()
        central_widget.setLayout(qvbox)
        self.setCentralWidget(central_widget)

        for label in [self.P_A_label, self.H_A_label, self.P_B_label, self.H_B_label, self.T_counts_label, self.H_T_label,
                      self.P_joint_label, self.H_AB_label, self.H_A_given_B_label, self.H_B_given_A_label]:
            label.setAlignment(Qt.AlignCenter)

        # Set objects name
        self.P_A_label.setObjectName("P_A_label")
        self.P_B_label.setObjectName("P_B_label")
        self.T_counts_label.setObjectName("T_counts_label")
        self.P_joint_label.setObjectName("P_joint_label")
        self.H_A_label.setObjectName("H_A_label")
        self.H_B_label.setObjectName("H_B_label")
        self.H_T_label.setObjectName("H_T_label")
        self.H_AB_label.setObjectName("H_AB_label")
        self.H_A_given_B_label.setObjectName("H_A_given_B_label")
        self.H_B_given_A_label.setObjectName("H_B_given_A_label")

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
            QLabel#P_A_label, QLabel#P_B_label, QLabel#T_counts_label, QLabel#P_joint_label {
                background-color: rgb(227, 218, 195);
                font-family: Helvetica;
                font-size: 18px;
                font-weight: bold;
                border: 3px solid;
                border-color: rgb(163, 144, 98);
                color: rgb(0,0,0);
                padding-left: 10px;
            }
            QLabel#H_A_label, QLabel#H_B_label, QLabel#H_T_label, 
            QLabel#H_AB_label, QLabel#H_A_given_B_label, QLabel#H_B_given_A_label {
                background-color: rgb(201, 227, 195);
                font-family: Helvetica;
                font-size: 18px;
                font-weight: bold;
                border: 3px solid;
                border-color: rgb(90, 122, 82);
                color: rgb(0,0,0);
                padding-left: 10px;
            }
        """)

        self.show()

    def compute_H_A_and_H_B(self):
        H_A = compute_entropy(self.P_A)
        H_B = compute_entropy(self.P_B)
        return H_A, H_B

    def compute_H_T(self):
        P_T = self.T_counts / self.T_counts.sum()
        return compute_entropy(P_T)

    def compute_joint_entropy(self):
        P_A_marginal = np.sum(self.P_joint, axis=1)
        P_B_marginal = np.sum(self.P_joint, axis=0)
        H_AB = compute_entropy(self.P_joint[self.P_joint > 0])
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