#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 07:25:29 2017

@author: Mathieu Villion
"""

import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMessageBox
from iiyama_x4071_lib import InputExtCode
from iiyama_x4071_lib import ONOFFCode
from iiyama_x4071_lib import X4071


class TimerMessageBox(QMessageBox):
    def __init__(self, MessageStr, timeout=3, parent=None):
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle("X4071 control")
        self.setStyleSheet(
            "QLabel{min-width:500 px; font-size: 24px; color:red}")
        self.time_to_wait = timeout
        self.setText(MessageStr)
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QTimer(self)
        self.timer.setInterval(timeout*1000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.close)
        self.timer.start()

    def closeEvent(self, event):
        event.accept()


def main():
    app = QApplication([])
    Screen = X4071("/dev/ttyUSB0")

    Command = sys.argv[1]

    if Command in ["mute"]:
        if not Screen.send_remote(Command):
            print("Command failed!")
        (_, Value) = Screen.ext_get_from_name(Command)
        MessageStr = "%s %s" % (Command, ONOFFCode[Value == 1])
    if Command in ["pip_preset_on"]:
        Screen.ext_get_set_from_name("input", InputExtCode[sys.argv[2]], 0.5)
        Screen.ext_get_set_from_name("Audio input", 4, 0.5)
        Screen.ext_get_set_from_name("PIP right", 1, 0.5)
        Screen.ext_get_set_from_name("PIP bottom", 0, 0.5)
        Screen.ext_get_set_from_name(
            "PIP input", InputExtCode[sys.argv[3]], 0.5)
        Screen.ext_get_set_from_name("PIP PBP", 1, 1)
        MessageStr = Command
    if Command in ["pip_preset_off"]:
        Screen.ext_get_set_from_name("PIP PBP", 0, 1.5)
        Screen.ext_get_set_from_name("input", InputExtCode[sys.argv[2]], 0.5)
        MessageStr = Command
    elif Command in ["vol+", "vol-"]:
        if not Screen.send_remote(Command):
            print("Command failed!")
        (_, Value) = Screen.ext_get_from_name("volume")
        MessageStr = "Volume %d%%" % Value

    messagebox = TimerMessageBox(MessageStr, 2)
    messagebox.exec_()
    app.quit()
    print("Done")


if __name__ == '__main__':
    main()
