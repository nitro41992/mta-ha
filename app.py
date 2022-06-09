import os
from datetime import datetime, timedelta
import sys


TIME_TO_GO_DOWNSTAIRS = '3:00'
TIME_TO_STOP = '5:00'
TIME_TO_STATION = '1:00'
FMT = '%H:%M'
NUMBER_OF_FUTURE_TIMES = 1

now = datetime.now()
current_time = now.strftime(FMT)
# print("Current Time =", current_time)

train = sys.argv[1]
station = sys.argv[2]

TIME_TO_GO_DOWNSTAIRS = datetime.strptime(TIME_TO_GO_DOWNSTAIRS,"%M:%S")
TIME_TO_STOP = datetime.strptime(TIME_TO_STOP,"%M:%S")
TIME_TO_STATION = datetime.strptime(TIME_TO_STATION,"%M:%S")
DELTA_TO_GO_DOWNSTAIRS = timedelta(hours=TIME_TO_GO_DOWNSTAIRS.hour, minutes=TIME_TO_GO_DOWNSTAIRS.minute, seconds=TIME_TO_GO_DOWNSTAIRS.second)
DELTA_TO_STOP = timedelta(hours=TIME_TO_STOP.hour, minutes=TIME_TO_STOP.minute, seconds=TIME_TO_STOP.second)
DELTA_TO_STATION = timedelta(hours=TIME_TO_STATION.hour, minutes=TIME_TO_STATION.minute, seconds=TIME_TO_STATION.second)
total_delta = DELTA_TO_GO_DOWNSTAIRS + DELTA_TO_STOP + DELTA_TO_STATION

stops_and_times_dict = {}
stops_and_times = os.popen(f"underground stops {train} | grep L06").read().split('\n')[:-1]
for stop in stops_and_times:
    station_and_times = stop.split(' ')
    key = station_and_times[0]
    times_list = []
    for item in station_and_times[1:]:
        
        time_before_train_arrives = datetime.strptime(item, FMT) - total_delta
        if time_before_train_arrives > datetime.strptime(current_time,"%H:%M"):
            string_time_before_train_arrives = time_before_train_arrives.strftime("%I:%M %p")
            # print(f'Leave at {string_time_before_train_arrives} and get there by {item}')
            times_list.append(string_time_before_train_arrives)

    stops_and_times_dict[key] = times_list[:NUMBER_OF_FUTURE_TIMES]
print(stops_and_times_dict[station][0])