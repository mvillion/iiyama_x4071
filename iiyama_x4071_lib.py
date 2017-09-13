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

# ______________________________________________________________________________
STX = b'\x02'
ETX = b'\x03'

InputExtCode = \
    {
        "no_mean": 0,
        "D-SUB": 1,
        "Reserved": 2,
        "HDMI1": 3,
        "HDMI3": 4,
        "composite": 5,
        "S-video": 7,
        "option": 8,
        "DisplayPort": 9,
        "YPbPr": 12,
        "HDMI2": 18,
    }

LanguageCode = \
    {
        1: "english",
        2: "french",
        3: "german",
        4: "dutch",
        5: "polish",
        6: "czech",
        7: "italian",
        8: "russian",
        9: "japanese",
        10: "chinese",
        11: "chinese (traditional)",
    }

# note: 2nd argument: accept read operation
# note: 3rd argument: accept write operation
# note: some write only commands may be missing
Page00OPCode = \
    {
        0x04: ("factory reset", 0, 0),
        0x06: ("screen reset", 0, 0),
        0x08: ("picture reset", 0, 0),
        0x0e: ("clock", 1, 1),
        0x0c: ("color temperature (2)", 0, 0),
        0x10: ("brightness", 1, 1),
        0x12: ("contrast", 1, 1),
        0x14: ("reserved", 0, 0),
        0x16: ("user color red", 1, 1),
        0x18: ("user color green", 1, 1),
        0x1a: ("user color blue", 1, 1),
        0x1e: ("auto setup", 0, 0),
        0x20: ("H position", 1, 1),
        0x30: ("V position", 1, 1),
        0x3e: ("clock phase", 1, 1),
        0x60: ("input", 1, 1),
        0x62: ("volume", 1, 1),
        0x68: ("language", 1, 1),
        0x8c: ("sharpness", 1, 1),
        0x8d: ("mute", 1, 1),
        0x8f: ("treble", 0, 0),
        0x90: ("Tint", 0, 0),
        0x91: ("bass", 0, 0),
        0x92: ("black level", 0, 0),
        0x93: ("balance", 0, 0),
        0xc9: ("firmware version", 1, 0),
        0xe1: ("power save", 0, 0),
        0xe3: ("control lock", 1, 0),
        0xfc: ("OSD turn off", 1, 0),
    }
#        0xxx: "configuration reset",
Name2PageOPCode = {}
for (k, v) in Page00OPCode.items():
    Name2PageOPCode[v[0]] = (0x00, k)

GammaSelectionCode = \
    {
        1: "native",
        4: "gamma 2.2",
        5: "option",
        7: "S gamma",
        8: "gamma 2.4",
    }

ZoomModeCode = \
    {
        1: "real",
        2: "custom",
        5: "dynamic",
        6: "normal",
        7: "full",
    }

ColorSystemCode = \
    {
        1: "NTSC",
        2: "PAL",
        3: "SECAM",
        4: "auto",
        5: "4.43NTSC",
        6: "PAL-60",
    }

SideColorCode = \
    {
        0: "black",
        1: "middle",
        2: "white",
    }

OSDRotationCode = \
    {
        0: "off",
        1: "90",
        2: "H mirror",
        3: "V mirror",
        4: "180",
        5: "270",
    }
Name2OSDRotation = dict(map(reversed, OSDRotationCode.items()))

PIPCOde = \
    {
        1: "off",
        2: "PIP",
        4: "still",
    }

Page02OPCode = \
    {
        0x1b: ("picture mode", 1, 1),
        0x20: ("color", 0, 0),
        0x21: ("noise reduction", 0, 0),
        0x22: ("color system", 0, 0),
        0x23: ("black level expansion", 0, 0),
        0x24: ("film mode", 0, 0),
        0x26: ("scan conversion", 0, 0),
        0x2c: ("OFF timer", 0, 0),
        0x2f: ("Audio input", 1, 1),
        0x39: ("OSD H position", 1, 1),
        0x3a: ("OSD V position", 1, 1),
        0x3e: ("information OSD", 0, 0),
        0x3f: ("monitor ID", 1, 1),
        0x40: ("IR control", 1, 1),
        0x41: ("input detect", 0, 0),
        0x42: ("OSD rotation", 1, 1),
        0x51: ("H resolution", 0, 0),
        0x52: ("V resolution", 0, 0),
        0x69: ("gamma selection", 0, 0),
        0x6d: ("zoom H-Expansion", 0, 0),
        0x6e: ("zoom V-Expansion", 0, 0),
        0x72: ("PIP size", 1, 1),
        0x73: ("PIP PBP", 1, 1),
        0x74: ("PIP input", 1, 1),
        0x75: ("PIP right", 1, 1),
        0x76: ("PIP bottom", 1, 1),
        0x77: ("still capture", 0, 0),
        0x79: ("select temperature sensor", 0, 0),
        0x80: ("hours running", 0, 0),
        0x7a: ("readout a temperature", 0, 0),
        0x7e: ("cooling fan", 0, 0),
        0xcd: ("zoom H-Position", 0, 0),
        0xce: ("zoom V-Position", 0, 0),
        0xcf: ("zoom mode", 1, 1),
        0xd1: ("tiling H monitor", 0, 0),
        0xd2: ("tiling V monitor", 0, 0),
        0xd3: ("tiling position", 0, 0),
        0xd4: ("tiling mode", 0, 0),
        0xd6: ("tiling frame comp.", 0, 0),
        0xd9: ("power on delay.", 0, 0),
        0xdb: ("input resolution", 0, 0),
        0xdc: ("screen saver gamma", 0, 0),
        0xdd: ("screen saver brightness", 0, 0),
        0xde: ("screen saver motion", 0, 0),
        0xe0: ("side border color", 0, 0),
        0xe4: ("scan mode", 0, 0),
        0xe5: ("advanced option reset", 1),
        0xfe: ("control the closed caption function", 0, 0),
    }
#        0xxx: "PIP audio",
#        0xxx: "PIP reset",
for (k, v) in Page02OPCode.items():
    Name2PageOPCode[v[0]] = (0x02, k)

# page 01 are commands
Page01OPCode = \
    {
        0xd6: ("power status", 0),
    }

# page c2 are date and time commands
# reply on page c3
Pagec2OPCode = \
    {
        0x11: ("read datetime", 1),
        0x12: ("write datetime", 0),
        0x13: ("read schedule", 1),
        0x14: ("write schedule", 0),
        0x16: ("read serial number", 1),
        0x17: ("read model name", 1),
    }
Name2CommandCode = {}
for (k, v) in Pagec2OPCode.items():
    Name2CommandCode[v[0]] = (0xc2, k)

# command codes are single octet
CommandCode = \
    {
        0x0c: "save current settings",
        0xb1: "self diagnosis",
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

# ______________________________________________________________________________
    def ext_has_answer(self, Page, OPCode):
        Answer = self.send_ext_cmd(b"A0C", b"%02x%02x" % (Page, OPCode))
        return Answer != b"BE"

    def ext_get(self, Page, OPCode):
        Answer = self.send_ext_cmd(b"A0C", b"%02x%02x" % (Page, OPCode))
        Parsed = self.parse_get_parameter_replay(Answer)
        if Parsed is None:
            return None
        (PageOut, OPCodeOut, Type, MaxValue, CurrentValue) = Parsed
        if Page != PageOut or OPCode != OPCodeOut:
            print("wrong page, opcode")
#            return None
        return (MaxValue, CurrentValue)

    def ext_get_from_name(self, Name):
        (Page, OPCode) = Name2PageOPCode[Name]
        return self.ext_get(Page, OPCode)

    def ext_command(self, Page, OPCode):
        Answer = self.send_ext_cmd(b"A0A", b"%02x%02x" % (Page, OPCode))
        return Answer

    def ext_command_from_name(self, Name):
        (_, OPCode) = Name2CommandCode[Name]
        Answer = self.send_ext_cmd(b"A0A", b"c2%02x" % OPCode, 0.1)
        return Answer

    def ext_set(self, Page, OPCode, Value, delay=0.08):
        Answer = self.send_ext_cmd(
            b"A0E", b"%02x%02x%04x" % (Page, OPCode, Value), delay)
        Parsed = self.parse_get_parameter_replay(Answer)
        if Parsed is None:
            return None
        (PageOut, OPCodeOut, Type, MaxValue, CurrentValue) = Parsed
        if Page != PageOut or OPCode != OPCodeOut:
            print("wrong page, opcode")
#            return None
        return (MaxValue, CurrentValue)

    def ext_set_from_name(self, Name, Value, delay=0.08):
        (Page, OPCode) = Name2PageOPCode[Name]
        return self.ext_set(Page, OPCode, Value, delay)

    def ext_get_set_from_name(self, Name, Value, delay=0.08):
        Metric = self.ext_get_from_name(Name)
        if Metric is None:
            return False
        (Max, ReadValue) = Metric
        print("%s %d / %d" % (Name, ReadValue, Max))
        if ReadValue == Value:
            return True
        Metric = self.ext_set_from_name(Name, Value, delay=delay)
        if Metric is None:
            return False
        (Max, ReadValue) = Metric
        print("%s %d / %d" % (Name, ReadValue, Max))
        if ReadValue == Value:
            return True

    def bcc(self, Vect):
        Sum = 0
        for b in Vect:
            Sum ^= b
        return Sum

    def parse_get_parameter_replay(self, Message):
        Result = int(Message[0:2], 16)
        if Result != 0:
            return None
        Page = int(Message[2:4], 16)
        OPCode = int(Message[4:6], 16)
        Type = int(Message[6:8], 16)
        MaxValue = int(Message[8:12], 16)
        CurrentValue = int(Message[12:16], 16)
        return (Page, OPCode, Type, MaxValue, CurrentValue)

    def send_ext_cmd(self, Header, Message, delay=0.08):
        Message = STX+Message+ETX
        Header = STX+b"IYA"+Header+b"%02X" % len(Message)
        Cmd = Header+Message
        Cmd += bytes([self.bcc(Cmd[1:-1])])+b'\r'
#        print(Cmd)
        self.Ser.write(Cmd)
        sleep(delay)
        if self.Ser.in_waiting == 0:
            print("no answer")
            return None
        Answer = self.Ser.read(self.Ser.in_waiting)
        if len(Answer) == 0:
            print("no answer2")
            return None
        # note: BCC output by screen is fixed to 0x0e and obviously wrong
#        BCCInput = Answer[1:-3]
#        print(BCCInput)
#        BCC = self.bcc(BCCInput)
#        if BCC != Answer[-2]:
#            print("wrong BCC %02x %02x" % (BCC, Answer[-2]))
#            print(Answer)
#        if Answer[:6] != STX+b'IYAAD':
#            print("wrong header start %s" % Answer)
        Len = int(Answer[6:8], 16)
        if Len+2+8 != len(Answer):
            print("wrong length")
        return Answer[9:-3]

    def read_serial_number(self):
        Cmd = "read serial number"
        Answer = self.ext_command_from_name(Cmd)
        if Answer[:4] != b"C3%02X" % Name2CommandCode[Cmd][1]:
            return "<wrong serial number>"
        return Answer[4:]

    def read_model_name(self):
        Cmd = "read model name"
        Answer = self.ext_command_from_name(Cmd)
        if Answer[:4] != b"C3%02X" % Name2CommandCode[Cmd][1]:
            return "<wrong model name>"
        return Answer[4:]

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

#    for Page in range(256):
#        print("_____%02x____" % Page)
#        for k in range(256):
#            if not Screen.ext_has_answer(Page, k):
#                continue
#            print("%02x" % k)

    print("____extended command for page 00_____")
    for (k, v) in Page00OPCode.items():
        if v[1] == 0:
            continue
        Metric = Screen.ext_get(0x00, k)
        if Metric is None:
            print(v[0])
            continue
        (Max, Value) = Metric
        print("%s %d / %d" % (v[0], Value, Max))

    print("____extended command for page 02_____")
    for (k, v) in Page02OPCode.items():
        if v[1] == 0:
            continue
        Metric = Screen.ext_get(0x02, k)
        if Metric is None:
            print(v[0])
            continue
        (Max, Value) = Metric
        print("%s %d / %d" % (v[0], Value, Max))

#    print("____extended command for page c2_____")
#    for (k, v) in Pagec2OPCode.items():
#        if v[1] == 0:
#            continue
#        Metric = Screen.ext_command(0xc2, k)
#        if Metric is None:
#            print(v[0])
#            continue
#        print("%s %s" % (v[0], Metric))

#    print("____extended command tests_____")
#    for BrightnessPercent in [99, 40]:
#        print("setting brightness to %d%%" % BrightnessPercent)
#        Screen.ext_set_from_name("brightness", BrightnessPercent)
#        sleep(1)

    print("serial number is %s" % Screen.read_serial_number().decode("utf-8"))
    print("model name is %s" % Screen.read_model_name().decode("utf-8"))

#    # circle on PIP positions
#    for (rl, bu) in [(0, 0), (0, 1), (1, 1), (1, 0)]:
#        Screen.ext_set_from_name("PIP right", rl, 1.5)
#        Screen.ext_set_from_name("PIP bottom", bu, 1.5)
#
#    Screen.ext_set_from_name("PIP PBP", 2, 1)
