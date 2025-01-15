from esp32sensor import BLESensor
import asyncio
import time
sensor = BLESensor("COM3")

sensor.open()


async def main():
    task1 = asyncio.create_task(sensor.read_beacon(10))
    ret1 = await task1
    await asyncio.sleep(0.5)
    task2 = asyncio.create_task(sensor.read_sensor())
    ret2 = await task2

    print(ret1)
    print(ret2)

asyncio.run(main())