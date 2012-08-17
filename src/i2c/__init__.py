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

        #TODO: verify that we can open the file here, so we fail early.

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
        self.fd = posix.open(file_path, posix.O_RDWR)

        if ioctl(self.fd, I2C_SLAVE, addr) != 0:
            raise Exception() #TODO: add more exceptions.

    def __getitem__(self, key):
        addr = struct.pack('B', key)
        if posix.write(self.fd, addr) != 1:
            raise Exception()

        ret_val = struct.unpack('B', posix.read(self.fd, 1))[0]

        return ret_val

    def __setitem__(self, key, value):
        msg = struct.pack('BB', key, value)

        if posix.write(self.fd, msg) != 2:
            raise Exception()

    def __del__(self):
        try:
            posix.close(self.fd)
        except AttributeError:
            pass #Do nothing in this case.
