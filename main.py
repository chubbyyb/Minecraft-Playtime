import os
from datetime import datetime

files = ['2023-08-13-1.log', '2023-08-13-2.log', '2023-08-13-3.log', '2023-08-13-4.log']
combined_file = 'combined.log'
playersOn = {}  # Use an empty dictionary to track players' login times
playersTime = {}  # Use an empty dictionary to track players' total time

def getTimeDifference(timestamp1, timestamp2):
    time_format = "%H:%M:%S"
    dt1 = datetime.strptime(timestamp1, time_format)
    dt2 = datetime.strptime(timestamp2, time_format)

    # Calculate the time difference
    time_difference = dt2 - dt1
    return time_difference.total_seconds()

# Combine all files in the list
with open(combined_file, 'w') as outfile:
    for fname in files:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

with open(combined_file) as f:
    lines = f.readlines()
    for line in lines:
        if "Server thread/INFO" in line:
            if "joined" in line:
                time = line[1:9]
                username = (line.split(": ", 2)[1]).split()[0]
                playersOn[username] = time
                if username not in playersTime:
                    playersTime[username] = 0
            elif "left" in line:
                time = line[1:9]
                username = (line.split(": ", 2)[1]).split()[0]
                if username in playersOn:
                    time_diff = getTimeDifference(playersOn[username], time)
                    playersTime[username] += time_diff

for key, value in sorted(playersTime.items(), key=lambda item: item[1], reverse=True):
    print(key, str(round((value/60), 2)) + " minutes")

