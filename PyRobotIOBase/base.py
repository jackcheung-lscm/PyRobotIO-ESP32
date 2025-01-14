from abc import ABC, abstractmethod


class RobotIOBase(ABC):
    def __init__(self, device_id: str, **kwargs):
        """
        Initialize the robot IO with a unique device identifier.

        Parameters:
        - device_id (str): Unique identifier for the device.
        - **kwargs: Additional keyword arguments for device-specific settings.
        """
        self.device_id = device_id
        self.is_open = False

    @abstractmethod
    def open(self, **kwargs):
        """
        Open the connection to the device.
        """
        pass

    @abstractmethod
    def read(self, **kwargs):
        """
        Read data from the device.

        Returns:
        - data: Device data in a standardized format.
        """
        pass

    @abstractmethod
    def reset(self, **kwargs):
        """
        Reset the device to its default state.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the connection to the device.
        """
        pass
