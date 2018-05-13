import pigpio


class I2cError(Exception):
    pass


class PigI2cBus(dict):

    def __init__(self, pi, sda_pin, scl_pin, baud=50000):
        self.pi = pi
        pi.set_pull_up_down(sda_pin, pigpio.PUD_UP)
        pi.set_pull_up_down(scl_pin, pigpio.PUD_UP)

        pi.bb_i2c_open(sda_pin, scl_pin, baud)

        self.handle = sda_pin

        dict.__init__(self)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def __getitem__(self, key):
        if not isinstance(key, (int, long)):
            raise NotSupportedError()

        if not 0 <= key <= 255:
            raise IndexError()

        if key in self:
            return dict.__getitem__(self, key)
        else:
            device = BBI2cDevice(self.pi, self.handle, key)
            dict.__setitem__(self, key, device)
            return device

    def __setitem___(self, key):
        raise NotSupportedError()

    def close(self):
        self.pi.bb_i2c_close(self.handle)


class BBI2cDevice(object):

    def __init__(self, pi, i2c_handle, addr):
        self.pi = pi
        self.handle = i2c_handle
        self.addr = addr

    def check_key(self, key):
        if not isinstance(key, (int, long)):
            raise NotSupportedError()

        if not 0 <= key <= 255:
            raise IndexError()

    def __getitem__(self, key):
        self.check_key(key)

        cmd = [4, self.addr] # Set address
        cmd += [2, 7, 1, key] # write the register to read.
        cmd += [2, 6, 1] # read 1 byte
        cmd += [3, 0] # stop and end sequence

        (count, data) = self.pi.bb_i2c_zip(self.handle, cmd)

        if count < 1:
            raise I2cError(pigpio.error_text(count))

        return data

    def __setitem__(self, key, value):
        self.check_key(key)
        self.check_key(value)

        cmd = [4, self.addr] # Set address
        cmd += [2, 7, 2, key, value] # write the register then value .
        cmd += [3, 0] # stop and end sequence

        (count, data) = self.pi.bb_i2c_zip(self.handle, cmd)


