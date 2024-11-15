### 1. Install Dependencies

Run the following command to install the robotio_base package and other dependencies:

```bash
pip install -e .
```

### 2. Implement Your Sensor

```python
from PyRobotIOBase.base import RobotIOBase
from PyRobotIOBase.exceptions import ConnectionError, ReadError, DeviceError


class MySensor(RobotIOBase):
    def __init__(self, device_id: str, **kwargs):
        super().__init__(device_id, **kwargs)
        # Initialize sensor-specific attributes here
        self.connection = None

    def open(self, **kwargs):
        # Implement code to open connection to your sensor
        try:
            # Example: self.connection = open_sensor_connection()
            self.is_open = True
            print("Sensor is open.")
        except Exception as e:
            raise ConnectionError(f"Failed to open sensor: {e}")

    def read(self, **kwargs):
        # Implement code to read data from your sensor
        if not self.is_open:
            raise ConnectionError("Sensor is not open.")
        try:
            # Example: data = self.connection.read_data()
            data = {"temperature": 25.0}  # Replace with actual sensor data
            return data
        except Exception as e:
            raise ReadError(f"Failed to read sensor data: {e}")

    def reset(self, **kwargs):
        # Implement code to reset your sensor
        if not self.is_open:
            raise ConnectionError("Sensor is not open.")
        try:
            # Example: self.connection.reset()
            pass
        except Exception as e:
            raise DeviceError(f"Failed to reset sensor: {e}")

    def close(self):
        # Implement code to close connection to your sensor
        if self.is_open:
            try:
                # Example: self.connection.close()
                self.is_open = False
            except Exception as e:
                raise DeviceError(f"Failed to close sensor: {e}")
```


## 3. Example Implementation

### 3.1. IAQSensor Class

```python
# iaq_sensor/iaq_sensor.py

from PyRobotIOBase.base import RobotIOBase
from PyRobotIOBase.exceptions import ConnectionError, ReadError, TimeoutError, DeviceError
import serial
import json

class IAQSensor(RobotIOBase):
    def __init__(
        self,
        device_id: str,
        port: str = '/dev/ttyUSB0',
        baudrate: int = 115200,
        timeout: float = 1.0,
        **kwargs
    ):
        """
        Initialize the IAQ sensor.

        Parameters:
        - device_id (str): Unique identifier for the sensor.
        - port (str): Serial port name.
        - baudrate (int): Communication baud rate.
        - timeout (float): Read timeout in seconds.
        - **kwargs: Additional configuration parameters.
        """
        super().__init__(device_id, **kwargs)
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None

    def open(self):
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            self.is_open = True
        except serial.SerialException as e:
            raise ConnectionError(f"Failed to open serial port {self.port}: {e}")

    def read(self, timeout: float = None) -> dict:
        if not self.is_open:
            raise ConnectionError("Sensor is not open.")
        if timeout is not None:
            self.serial_conn.timeout = timeout
        try:
            raw_data = self.serial_conn.readline()
            if not raw_data:
                raise TimeoutError("Read operation timed out.")
            message = raw_data.decode('utf-8').strip()
            data_dict = json.loads(message)
            return data_dict
        except serial.SerialException as e:
            raise ReadError(f"Serial communication error: {e}")
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise ReadError(f"Failed to parse sensor data: {e}")

    def reset(self):
        if not self.is_open:
            raise ConnectionError("Sensor is not open.")
        reset_command = json.dumps({
            "device_id": self.device_id,
            "message_type": "command_request",
            "command": {
                "command_code": "reset",
                "parameters": {}
            }
        }) + '\n'
        self.serial_conn.write(reset_command.encode('utf-8'))

    def close(self):
        if self.is_open and self.serial_conn:
            self.serial_conn.close()
            self.is_open = False

```

### 3.2. Defining Parameter Types and Error Handling

- **Parameter Types**: Use type hints for all parameters.
- **Error Handling**: Raise custom exceptions defined in the `sensor_base.exceptions` module.

### 3.3. Usage Example

```python
from iaq_sensor.iaq_sensor import IAQSensor
from PyRobotIOBase.exceptions import ConnectionError, ReadError, TimeoutError

# Initialize the IAQ sensor with parameters
iaq_sensor = IAQSensor(
    device_id='iaq_sensor_01',
    port='/dev/ttyUSB1',
    baudrate=9600,
    timeout=2.0
)

try:
    iaq_sensor.open()
    data = iaq_sensor.read(timeout=2.0)
    print(f"Sensor Data: {data}")
except ConnectionError as ce:
    print(f"Connection error: {ce}")
except ReadError as re:
    print(f"Read error: {re}")
except TimeoutError as te:
    print(f"Timeout error: {te}")
finally:
    iaq_sensor.close()

```

## 4. Setup Github secrets for runner with name `PYROBOTIO_BASE_DEPLOY_KEY`

```text
Repository > Settings > Secrets and variables > Actions > Secrets > New repository secrets:
Name: |
PYROBOTIO_BASE_DEPLOY_KEY
Secret: |
-----BEGIN OPENSSH PRIVATE KEY-----
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
......
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
-----END OPENSSH PRIVATE KEY-----
```
