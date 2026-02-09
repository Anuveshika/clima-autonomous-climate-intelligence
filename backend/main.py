from fastapi import FastAPI
import asyncio
import threading

from scheduler import start_scheduler
from state import latest_result
from agents.climate_monitor import latest_result
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (hackathon safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    # Run scheduler in background thread
    threading.Thread(target=lambda: asyncio.run(start_scheduler()), daemon=True).start()


@app.get("/incident")
def get_incident():
    return latest_result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


#import asyncio
#from scheduler import start_scheduler

#if __name__ == "__main__":
#    asyncio.run(start_scheduler())
