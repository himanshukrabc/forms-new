import logging
import datetime
import asyncio

from logging.handlers import RotatingFileHandler

def create_rotating_handler(log_file, level):
    handler = RotatingFileHandler(log_file, mode='a', maxBytes=1024 * 1024 * 10 , backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(level)
    return handler


error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = create_rotating_handler('./logs/error_logs.log', logging.ERROR)
error_logger.addHandler(error_handler)


info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)
info_handler = create_rotating_handler('./logs/info_logs.log', logging.INFO)
info_logger.addHandler(info_handler)


requests = [(datetime.datetime.now(),200)]
cur_req = {}
cur_req[200]=1
cur_req[400]=0
cur_req[500]=0
past_req = {}
past_req[200]=1
past_req[400]=0
past_req[500]=0

# The request array stores the requests statuses in the last minute and the timestamp at which the reqest was maade.
# The requests whose timestamps are more than a minute old are removed. Thus the array only contains the 
# requests dispatched in last minute. Thus we can calculate the fractions of each type of statuses dispatched.
async def push_req(cur_time,status):
    print(cur_time,status)
    while(len(requests)!=0):
        print(requests[0][0])
        if(requests[0][0]-cur_time > datetime.timedelta(minutes=1)):
            cur_req[requests[0][1]]-=1
            requests.pop(0)
            past_req[requests[0][1]]+=1
        else:
            break
    requests.append((cur_time,status))
    cur_req[status]+=1

async def log_info(endpoint, method, data, status, response):
    task = asyncio.create_task(push_req(datetime.datetime.now(),status))
    info_logger.info(f"Response sent - Endpoint: {endpoint}, Method: {method}, Data:{data}, status: {status}, Response: {response}")

async def log_error(endpoint, method, data, error, status):
    task = asyncio.create_task(push_req(datetime.datetime.now(),status))
    error_logger.error(f"Endpoint: {endpoint}, Method: {method}, Data:{data}, Some error ocoured:",exc_info=error)

# Calculates the ratio of statuses dispatched.
def get_ratios():
    return {
        "average_percentage_of_statuses_dispatched":{
            200:round((100*(past_req[200]+cur_req[200])/(past_req[200]+cur_req[200]+past_req[400]+cur_req[400]+past_req[500]+cur_req[500])),2),
            400:round((100*(past_req[400]+cur_req[400])/(past_req[200]+cur_req[200]+past_req[400]+cur_req[400]+past_req[500]+cur_req[500])),2),
            500:round((100*(past_req[500]+cur_req[500])/(past_req[200]+cur_req[200]+past_req[400]+cur_req[400]+past_req[500]+cur_req[500])),2)
        },
        "number_of_statuses_dispatched_in_the_last_1_miute":{
            200:round(100*(cur_req[200]/len(requests)),2),
            400:round(100*(cur_req[400]/len(requests)),2),
            500:round(100*(cur_req[500]/len(requests)),2)
        }
    }
