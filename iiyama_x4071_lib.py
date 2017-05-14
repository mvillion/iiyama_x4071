#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 17:55:52 2017

@author: Mathieu Villion
"""

from serial import Serial
from time import sleep

InputCode = \
    {
        'HDMI1': b"r1",
        'HDMI2': b"r7",
        'HDMI3': b"r2",
        'D-SUB': b"r3",
        'OPTION': b"r5",
        'DisplayPort': b"r6",
        'VIDEO': b"v1",
        'YPbPr': b"v2",
        'S-VIDEO': b"v3",
        '(Input unkown)': None,
    }
InputName = dict(map(reversed, InputCode.items()))

PictureModeCode = \
    {
        'off': b"p0",
        'standard': b"p1",
        'game': b"p2",
        'cinema': b"p3",
        'scenary': b"p4",
        'text': b"p5",
        '(PictureMode unkown)': None,
    }
PictureModeName = dict(map(reversed, PictureModeCode.items()))

PowerCode = \
    {
        'ON': b"!",
        'OFF': b"\"",
        'FORCE_OFF': b"\"\"",
    }

# note: tested that there are no other valid codes
RemoteCode = \
    {
        'vol+': b"r06",
        'vol-': b"r07",
        'mute': b"ra6",
        'auto': b"r09",
        '(RemoteMode unkown)': None,
    }

ONOFFCode = \
    {
        False: "OFF",
        True: "ON",
        None: "(power status unknown)",
    }


class X4071():
    def __init__(self, TTY):
        self.Ser = Serial(TTY, 9600, timeout=1)

    def is_local_key_control_on(self):
        self.Ser.write(b"1048vL\r")
        sleep(0.1)
        if self.Ser.in_waiting == 0:
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        return Answer[6:7] == b"1"

    def is_power_on(self):
        self.Ser.write(b"1048vP\r")
        sleep(0.1)
        if self.Ser.in_waiting == 0:
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        return Answer[6:7] == b"1"

    def is_read_ir_control_on(self):
        self.Ser.write(b"1048vR\r")
        sleep(0.1)
        if self.Ser.in_waiting == 0:
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        return Answer[6:7] == b"1"

    def get_input_name(self):
        self.Ser.write(b"1048vI\r")
        sleep(0.1)
        if self.Ser.in_waiting == 0:
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        return InputName[Answer[6:-1]]

    def get_picture_mode(self):
        self.Ser.write(b"1048vM\r")
        sleep(0.1)
        if self.Ser.in_waiting == 0:
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        return PictureModeName[Answer[6:-1]]

    def get_brightness(self):
        self.Ser.write(b"1048vB\r")
        sleep(0.1)
        if self.Ser.in_waiting == 0:
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        return int(Answer[6:-1])

    def set_brightness(self, BrightnessPercent):
        return self.generic_cmd(b"1048_b%03d\r" % BrightnessPercent)

    def set_input(self, Option):
        if Option not in InputCode.keys():
            print("invalid input name")
            return None
        return self.generic_cmd(b"1048_%s\r" % InputCode[Option])

    def set_ir_control(self, isOn):
        if type(isOn) is not bool:
            print("invalid ir control option")
            return None
        return self.generic_cmd(b"1048_i%d\r" % isOn, 1)

    def set_local_key_control(self, isOn):
        if type(isOn) is not bool:
            print("invalid local key control option")
            return None
        return self.generic_cmd(b"1048_k%d\r" % isOn, 1)

    def set_power(self, Option):
        if Option not in PowerCode.keys():
            print("invalid power option")
            return None
        return self.generic_cmd(b"1048%s\r" % PowerCode[Option], 1)

    def send_remote(self, Option):
        if Option not in RemoteCode.keys():
            print("invalid power option")
            return None
        return self.generic_cmd(b"1048%s\r" % RemoteCode[Option], 1)

    def generic_cmd(self, Cmd, delay=0.1):
        self.Ser.write(Cmd)
        sleep(delay)
        if self.Ser.in_waiting == 0:
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        return Cmd == Answer

    def check_answer(self, Cmd):
        if self.Ser.in_waiting == 0:
            print(Cmd)
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        return Cmd == Answer

if __name__ == '__main__':
    Screen = X4071("/dev/ttyUSB0")

    print("Screen is %s" % ONOFFCode[Screen.is_power_on()])
    print("Input is %s" % Screen.get_input_name())
    print("Picture mode is %s" % Screen.get_picture_mode())
    print("Brightness is %d%%" % Screen.get_brightness())
    print(
        "Lock key control is %s" % ONOFFCode[Screen.is_local_key_control_on()])
    print("Lock IR control is %s" % ONOFFCode[Screen.is_read_ir_control_on()])

    for BrightnessPercent in [99, 40]:
        print("setting brightness to %d%%" % BrightnessPercent)
        Screen.set_brightness(BrightnessPercent)
        sleep(1)

    Option = True
    print("set IR control %d" % Option)
    if not Screen.set_ir_control(Option):
        print("Command failed!")
    sleep(1)

    Option = True
    print("set local key control %d" % Option)
    if not Screen.set_local_key_control(Option):
        print("Command failed!")
    sleep(1)

    for Option in ["mute", "vol+", "vol-"]:
        print("sending remote option %s" % Option)
        if not Screen.send_remote(Option):
            print("Command failed!")
        sleep(1)

#    for Option in ["HDMI3", "HDMI1"]:
#        print("setting input to %s" % Option)
#        if not Screen.set_input(Option):
#            print("Command failed!")
#        sleep(5)  # needed according to spec

#    for Option in ["OFF", "ON"]:
#        print("setting input to %s" % Option)
#        if not Screen.set_power(Option):
#            print("Command failed!")
#        sleep(14)  # needed according to spec
