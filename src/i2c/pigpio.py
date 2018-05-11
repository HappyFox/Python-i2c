import pigpio


class PigI2cBus(dict):

    def __init__(self, pi, sda_pin, scl_pin, baud=50000):
        self.pi = pi
        pi.set_pull_up_down(sda_pin, pigpio.PUD_UP)
        pi.set_pull_up_down(scl_pin, pigpio.PUD_UP)

        self.handle = pi.bb_i2c_open(sda_pin, scl_pin, baud)

        dict.__init__(self)


    def __getitem__(self, key):
        if not isinstance(key, (int, long)):
            raise NotSupportedError()

        if not 0 <= key <= 255:
            raise IndexError()

        if key in self:
            return dict.__getitem__(self, key)
        else:
            device = I2cDevice(self.file_path, key)
            dict.__setitem__(self, key, device)
            return device

    def __setitem___(self, key):
        raise NotSupportedError()
