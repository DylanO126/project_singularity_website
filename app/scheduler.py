from datetime import datetime
import schedule
import time
from scan_uploads import channel_scan_for_keyword

#schedule.every(1).minutes.do(channel_scan_for_keyword)
schedule.every().day.at("08:00").do(channel_scan_for_keyword)
schedule.every().day.at("13:00").do(channel_scan_for_keyword)
schedule.every().day.at("20:00").do(channel_scan_for_keyword)

print("Scheduler triggered scan at", datetime.now())

while True:
    schedule.run_pending()
    time.sleep(60)
