from fastapi import FastAPI
from esp32fastapi import router  # The router already has a global sensor_instance

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)