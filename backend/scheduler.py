import asyncio
import traceback
from agents.climate_monitor import run_climate_cycle

INTERVAL = 180  # 1800 -- 30 minutes 

async def start_scheduler():

    print("CLIMA Scheduler started")

    while True:
        try:
            await run_climate_cycle()
        except Exception:
            traceback.print_exc()

        await asyncio.sleep(INTERVAL)
