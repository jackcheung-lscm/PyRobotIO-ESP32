<<<<<<< HEAD
# from PyRobotIOBase.base import RobotIOBase
# from PyRobotIOBase.exceptions import ConnectionError, ReadError, DeviceError
from exceptions import ConnectionError, ReadError, DeviceError, WriteError

import serial
import json
import threading 
import asyncio
import time 



class BLESensor():
    # def __init__(self, device_id: str, **kwargs):
    #     super().__init__(device_id, **kwargs)
    #     # Initialize sensor-specific attributes here
    #     self.connection = None

    def __init__(self, device_id: str, **kwargs):
        self.device_id = device_id 
        self.ser = None
        self.is_open = False
        self.thread = threading.Thread(target=self.read_serial)
        self.thread.daemon = True
        self.sensor_f = False
        self.sensor_json = None
        self.beacon_f = False 
        self.beacon_json = None 
        self.ser_busy = False 

    def open(self):
        # Implement code to open connection to your sensor
        try:
            # Example: self.connection = open_sensor_connection()
            self.ser = serial.Serial(self.device_id, 115200, timeout=3)
            time.sleep(2)
            self.is_open = self.ser.is_open
            self.thread.start()

        except Exception as e:
            raise ConnectionError(f"Failed to open device: {e}")
        
        return self.is_open 
    
    def read_serial(self):
        while self.is_open:
            if self.ser.in_waiting>2:
                incoming = self.ser.readline().decode('utf-8')
                # print("Raw incoming data:", incoming) 
                tempJson = json.loads(incoming)
                if tempJson["sensor"] == "EnvSensor":
                   
                    self.sensor_f = True
                    self.sensor_json = tempJson
                   

                elif tempJson["sensor"] == "beacon":
                    
                    self.beacon_f = True
                    self.beacon_json = tempJson
                   

    async def read_sensor(self):
        # Implement code to read data from your sensor
        if not self.is_open:
            raise ConnectionError("Connection is not open.")
        try:
            # Example: data = self.connection.read_data()
            tx_data = {}  # Replace with actual sensor data
            tx_data["operation"] = "sensor"
            tx_data=json.dumps(tx_data)            
            await self.__send_data(tx_data)
            couter = 0 
            while not self.sensor_f:
                couter = couter + 1 
                await asyncio.sleep(1)
                if couter > 10:
                    raise TimeoutError("Timeout while reading sensor data.")
            self.sensor_f = False
            return self.sensor_json
        except Exception as e:
            raise ReadError(f"Failed to read sensor data: {e}")


    async def read_beacon(self,duration):
        if not self.is_open:
            raise ConnectionError("Connection is not open.")
        try:
            # Example: data = self.connection.read_data()
            tx_data = {}  # Replace with actual sensor data
            tx_data["operation"] = "ble"          
            tx_data=json.dumps(tx_data)     
            await self.__send_data(tx_data)
            counter = 0 
            while not self.beacon_f:
                counter = counter + 1
                await asyncio.sleep(1)
                
                if counter > duration:
                    raise TimeoutError("Timeout while reading sensor data.")
            self.beacon_f = False
            return self.beacon_json

        except Exception as e:            
                raise ReadError(f"Failed to read sensor data: {e}")
    async def reset(self, **kwargs):
        # Implement code to reset your sensor
        if not self.is_open:
            raise ConnectionError("Sensor is not open.")
        try:
            # Example: self.connection.reset()
            tx_data = {}  # Replace with actual sensor data
            tx_data["operation"] = "reset"
            tx_data=json.dumps(tx_data)
            await self.__send_data(tx_data)
        except Exception as e:
            raise DeviceError(f"Failed to reset sensor: {e}")

    def close(self):
        # Implement code to close connection to your sensor
        if self.is_open:
            try:
                # Example: self.connection.close()
                self.is_open = False
                self.ser.close()
                self.thread.join()
            except Exception as e:
                raise DeviceError(f"Failed to close sensor: {e}")
        return True

    async def __send_data(self, data):
        # Implement code to send data to your sensor
        if not self.is_open:
            raise ConnectionError("Sensor is not open.")
        try:
            # Example: self.connection.send_data(data)
            while self.ser_busy:
                asyncio.sleep(1)
                print("Waiting for serial port to be available")
            print("Sending data:", data)
            self.ser_busy = True
            val = self.ser.write(data.encode(encoding='ascii'))
            print("Out waiting:", self.ser.out_waiting)
            print("Wrote:", val)
            self.ser.flush()
            self.ser_busy = False
        except Exception as e:
            raise DeviceError(f"Failed to send data to sensor: {e}")
=======
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
        device_id = sensor_instance.device_id
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
>>>>>>> 74a42ff962656df9713ac8346efeef1847d7c105
