Python-i2c
==========

A simple library for i2c buses on embedded linux, like the beaglebone and Raspberry Pi

Usage :

'
>>> import i2c
>>> bus = i2c.I2cBus(3)
>>> dev = bus[0x40]
>>> dev[0]
17
>>> dev[0] = 16
>>> dev[0]
16
>>> 
'
