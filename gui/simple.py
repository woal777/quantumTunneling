import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QMessageBox

from tunneling.solve import SolvingProblem
from tunneling.setting import pretty_plot
import numpy as np


class MyApp(QWidget):

    def __init__(self):
        super().__init__()

        self.x: np.ndarray
        self.y: np.ndarray
        self.button = QPushButton('plot', self)
        self.button2 = QPushButton('save', self)
        self.textEdits = [QTextEdit(self) for _ in range(4)]
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 907, 690)
        self.setBackground()
        self.setEditbox()
        self.setButton()

        self.setWindowTitle('Tunneling current')
        self.show()

    def setBackground(self):
        oImage = QImage('figure.png')
        sImage = oImage.scaled(QSize(907, 690))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(sImage))
        self.setPalette(palette)

    def setButton(self):
        self.setOption(self.button)
        self.setOption(self.button2)
        self.button2.move(120, 0)
        self.button.clicked.connect(self.btnPlotEvent)
        self.button2.clicked.connect(self.btnSaveEvent)

    def setEditbox(self):
        for i in self.textEdits:
            self.setOption(i)

        self.textEdits[0].move(130, 200)
        self.textEdits[0].setPlaceholderText('\u03C6_left')

        self.textEdits[1].move(560, 200)
        self.textEdits[1].setPlaceholderText('\u03C6_right')

        self.textEdits[2].move(350, 300)
        self.textEdits[2].setPlaceholderText('eff_m')

        self.textEdits[3].move(350, 600)
        self.textEdits[3].setPlaceholderText('thickness')
        self.textEdits[3].setFont(QFont('SansSerif', 18))

    @classmethod
    def setOption(cls, box: QWidget):
        box.setFont(QFont('SansSerif', 22))
        box.setFixedSize(QSize(120, 50))

    def btnPlotEvent(self):
        """
        Get values from gui and Plotting current
        :return:
        """
        try:
            arr = [float(r.toPlainText()) for r in self.textEdits]
        except ValueError:
            qm = QMessageBox(self)
            qm.setIcon(QMessageBox.Critical)
            qm.setText('Invalid input')
            qm.exec_()
            return 0
        s = SolvingProblem(1, *arr)
        s.set_temperature(300)
        self.x, self.y = s.main(-0.3, 0.3)
        plt = pretty_plot(10, 8)
        plt.plot(self.x, self.y)
        plt.xlabel(r'$\mathrm{bias (V)}$')
        plt.ylabel(r'$\mathrm{current (A/m^2)}$')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.show()

    def btnSaveEvent(self):
        """
        Get values from gui and Plotting current
        :return:
        """
        if type(self.x) == type(np.ndarray):
            output = np.zeros((len(self.x), 2))
            output[:, 0] = self.x
            output[:, 1] = self.y
            np.savetxt('output.dat', output, fmt='%12.8e')
        else:
            qm = QMessageBox(self)
            qm.setIcon(QMessageBox.Critical)
            qm.setText('there is no previous data')
            qm.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
