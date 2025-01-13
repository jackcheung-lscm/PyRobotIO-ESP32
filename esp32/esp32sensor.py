from fastapi import APIRouter, HTTPException, status, Body
from pydantic import BaseModel
import serial, json, threading, asyncio, time


router = APIRouter()

# Create one global sensor instance
sensor_instance = None

class BLESensor:
    def __init__(self, device_id: str = "COM4"):
        self.device_id = device_id
        self.ser = None
        self.is_open = False
        self.thread = threading.Thread(target=self.read_serial, daemon=True)
        self.sensor_f = False
        self.sensor_json = None
        self.beacon_f = False
        self.beacon_json = None
        self.ser_busy = False

    def read_serial(self):
        while self.is_open and self.ser:
            if self.ser.in_waiting > 2:
                incoming = self.ser.readline().decode('utf-8')
                tempJson = json.loads(incoming)
                if tempJson.get("sensor") == "EnvSensor":
                    self.sensor_f = True
                    self.sensor_json = tempJson
                elif tempJson.get("sensor") == "beacon":
                    self.beacon_f = True
                    self.beacon_json = tempJson

    async def __send_data(self, data):
        if not self.is_open:
            raise HTTPException(status_code=500, detail="Sensor is not open.")
        try:
            while self.ser_busy:
                await asyncio.sleep(1)
            self.ser_busy = True
            self.ser.write(data.encode("ascii"))
            self.ser.flush()
            self.ser_busy = False
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send data: {e}")

# Instantiate the sensor once (global)
sensor_instance = BLESensor()

@router.post("/open")
def open_device():
    try:
        device_id = "COM3"
        sensor_instance.ser = serial.Serial(device_id, 115200, timeout=3)
        sensor_instance.is_open = sensor_instance.ser.is_open
        if sensor_instance.is_open and not sensor_instance.thread.is_alive():
            sensor_instance.thread.start()
        return {"status": sensor_instance.is_open}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/read_sensor")
async def read_sensor():
    if not sensor_instance.is_open:
        raise HTTPException(status_code=400, detail="Connection is not open.")

    try:
        tx_data = {"operation": "sensor"}
        await sensor_instance.__send_data(json.dumps(tx_data))
        counter = 0
        while not sensor_instance.sensor_f:
            await asyncio.sleep(1)
            counter += 1
            if counter > 10:
                raise HTTPException(status_code=500, detail="Timeout while reading sensor data.")
        sensor_instance.sensor_f = False
        return sensor_instance.sensor_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read sensor data: {e}")

@router.post("/read_beacon")
async def read_beacon(payload: dict = Body(...)):
    duration = payload.get("duration", 10)
    if not sensor_instance.is_open:
        raise HTTPException(status_code=400, detail="Connection is not open.")

    try:
        tx_data = {"operation": "ble"}
        await sensor_instance.__send_data(json.dumps(tx_data))
        counter = 0
        while not sensor_instance.beacon_f:
            await asyncio.sleep(1)
            counter += 1
            if counter > duration:
                raise HTTPException(status_code=500, detail="Timeout while reading sensor data.")
        sensor_instance.beacon_f = False
        return sensor_instance.beacon_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read sensor data: {e}")

@router.post("/reset")
async def reset():
    if not sensor_instance.is_open:
        raise HTTPException(status_code=400, detail="Sensor is not open.")

    try:
        tx_data = {"operation": "reset"}
        await sensor_instance.__send_data(json.dumps(tx_data))
        return {"detail": "Reset command sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset sensor: {e}")

@router.post("/close")
def close_device():
    if sensor_instance.is_open:
        try:
            sensor_instance.is_open = False
            sensor_instance.ser.close()
            sensor_instance.thread.join()
            return {"detail": "Sensor closed."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to close sensor: {e}")
    else:
        return {"detail": "Sensor already closed."}

@router.get("/healthy", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK" if sensor_instance.ser and sensor_instance.ser.is_open else "Closed"}