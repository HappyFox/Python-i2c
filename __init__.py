import fcntl
import posix
import struct

from fcntl import ioctl

# from i2c-dev.h
I2C_SLAVE = 0x0703

class NotSupportedError(Exception):
    pass

class I2cBus(dict):

    def __init__(self, bus):
        self.bus = bus
        self.file_path = "/dev/i2c-%d" % self.bus

        dict.__init__(self)

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            device = I2cDevice(self.file_path, key)
            dict.__setitem__(self, key, device)
            return device

    def __setitem___(self, key):
        raise NotSupportedError()


class I2cDevice(object):

    def __init__(self, file_path, addr):
        self.file = posix.open(file_path, posix.O_RDWR)

        if ioctl(self.file, I2C_SLAVE, addr) != 0:
            raise Exception() #TODO: add more exceptions.

    def __getitem__(self, key):
        addr = struct.pack('B', key)
        if posix.write(self.file, addr) != 1:
            raise Exception()

        return posix.read(self.file, 1)

    def __setitem__(self, key):
        pass
