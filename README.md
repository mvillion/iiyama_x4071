# iiyama_x4071
Python code to use RS 323 connection of iiyama X4071 screen

iiyama X4071 screen comes with a serial port cable.
Using a USB to serial adapter, it is possible to get some status information and control some of the features of the screen.
iiyama documentation lists two types of commands: basic and extended.
Only basic commands are implemented in the code.
All basic commands have been tested successfully.

A few scenarios of usage:
- automatically switch input source at PC boot time
- map input source to a keyboard shortcut
- a third option to test/control the screen in case of keys failure or lost of IR remote
- possibility to lock keys and/or IR when the screen is left in a public place

Enjoy!
