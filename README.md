# iiyama_x4071
Python code to use RS 232 connection of iiyama X4071 screen

iiyama X4071 screen comes with a serial port cable.
Using a USB to serial adapter, it is possible to get some status information and control some of the features of the screen.
iiyama documentation lists two types of commands: basic and extended.
All basic commands have been tested successfully.

Most of extended commands (pages 0x00 and 0x02) are implemented.

A few scenarios of usage:
- automatically switch input source at PC boot time
- map input source to a keyboard shortcut (see iiyama_shortcut.py)
- a third option to test/control the screen in case of keys failure or lost of IR remote
- possibility to lock keys and/or IR when the screen is left in a public place
- using undocumented PIP/PBP mode 3, it is possible to display simultaneously 3 sources (the third being VGA)

Enjoy!
