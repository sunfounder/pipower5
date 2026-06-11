"""Device detection for PiPower5 HAT.

Provides is_connected() used by pironman5/pm_auto to detect whether the
PiPower5 UPS HAT is physically attached and responding on the I2C bus.
"""

import os

# Known I2C addresses for PiPower5 (varies by SPC firmware version)
_PIPOWER5_I2C_ADDRESSES = [0x5c, 0x57, 0x5a]


def is_connected():
    """Check if the PiPower5 I2C device is present and responding.

    The PiPower5 HAT communicates over I2C bus 1. The I2C address varies
    depending on the firmware version. Probes known addresses.

    As a fallback (e.g. smbus2 not installed), checks for the kernel
    device node /dev/pipower5.

    Returns:
        bool: True if the device is connected and responding, False otherwise.
    """
    if not os.path.exists('/dev/i2c-1'):
        return False

    try:
        from smbus2 import SMBus
        bus = SMBus(1)
        try:
            for addr in _PIPOWER5_I2C_ADDRESSES:
                try:
                    bus.read_byte_data(addr, 0)
                    return True
                except Exception:
                    continue
            return False
        finally:
            bus.close()
    except ImportError:
        pass

    # Fallback: raw I2C ioctl when smbus2 is not available
    try:
        import fcntl
        fd = os.open('/dev/i2c-1', os.O_RDWR)
        try:
            for addr in _PIPOWER5_I2C_ADDRESSES:
                try:
                    fcntl.ioctl(fd, 0x0703, addr)  # I2C_SLAVE
                    os.read(fd, 1)
                    return True
                except (OSError, IOError):
                    continue
            return False
        finally:
            os.close(fd)
    except Exception:
        pass

    # Last resort: check for kernel device node
    return os.path.exists('/dev/pipower5')
