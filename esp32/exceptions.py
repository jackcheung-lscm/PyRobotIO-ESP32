class DeviceError(Exception):
    """Base class for sensor exceptions."""
    pass


class ConnectionError(DeviceError):
    """Raised when a device connection fails."""
    pass


class TimeoutError(DeviceError):
    """Raised when a device read operation times out."""
    pass


class ReadError(DeviceError):
    """Raised when a device read operation fails."""
    pass

class WriteError(DeviceError):
    """Raised when a device write operation fails."""
    pass