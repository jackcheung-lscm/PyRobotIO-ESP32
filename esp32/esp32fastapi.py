from esp32sensor import BLESensor 
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import BaseModel

router = APIRouter()
sensor = BLESensor("/dev/ttyUSB0")


@router.post("/open")
def open_device():
    try:
        status = sensor.open()
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/read_sensor")
async def read_sensor():
    try:
        data = await sensor.read_sensor()
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read sensor data: {e}")

@router.post("/read_beacon")
async def read_beacon(payload: dict = Body(...)):
    duration = payload.get("duration", 10)
    try:
        data = await sensor.read_beacon(duration)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read sensor data: {e}")

@router.post("/reset")
async def reset():
    try:
        await sensor.reset()
        return {"message": "Sensor reset successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset sensor: {e}")   
    
@router.post("/close")
def close_device():
    try:
        status = sensor.close()
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to close sensor: {e}")
    
@router.get("/healthy", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK" if sensor.ser and sensor.ser.is_open else "Closed"}