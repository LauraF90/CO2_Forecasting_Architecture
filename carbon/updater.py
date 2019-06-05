from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Forecasts
from .scripts import scripts
# Background scheduler that empties the forecasts table every day at 00:00
def start():
    scheduler = BackgroundScheduler()
    s = scripts()
    scheduler.add_job(s.emptyForecasts,  'cron',year='*', month='*', day='*', week='*', day_of_week='*', hour=0, minute=0, second=0)
    scheduler.start()