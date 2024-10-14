
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pytz import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import sys
sys.path.append('~/app')

from database import engine, Base, setup_fts
from endpoints.item import router as router_item
from endpoints.item import scheduledItem
from endpoints.user import router as router_user
from endpoints.activity import router as router_activity
from endpoints.summary import router as router_summary


Base.metadata.create_all(bind=engine, checkfirst=True)
setup_fts()

app = FastAPI(title='Glitch', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()
scheduler.add_job(
    scheduledItem, 
    CronTrigger(hour=0, minute=0, timezone=timezone('Asia/Tokyo'))
)
scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

app.include_router(router_item, prefix='/api')
app.include_router(router_user, prefix='/api')
app.include_router(router_activity, prefix='/api')
app.include_router(router_summary, prefix='/api')
