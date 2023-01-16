from services.print_budget import refresh_budget, refresh_screen
import time
from dotenv import load_dotenv
import logging
import os
import threading
import buttons_dir

logging.basicConfig(level=logging.INFO)
load_dotenv()

monthly_budget = int(os.getenv('monthly_budget'))

def refresh_budget_thread(monthly_budget, _debug=False):
    refresh_budget(monthly_budget, _debug=False)
    time.sleep(1800)

def refresh_screen_thread():
    refresh_screen()
    time.sleep(175)

while True:

    api_pull=threading.Thread(target=refresh_budget,
                              args=(monthly_budget, _debug=False))
    screen_refresh=threading.Thread(target=refresh_screen_thread)

    button_listen=threading.Thread(target=buttons_dir.button_listen)

    api_pull.start()
    button_listen.start()
    time.sleep(180)
    screen_refresh.start()


    print('pause')