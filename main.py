import os
from datetime import datetime

files = ['2023-08-13-1.log', '2023-08-13-2.log', '2023-08-13-3.log', '2023-08-13-4.log']
combined_file = 'combined.log'
playersOn = {}  # Use an empty dictionary to track players' login times
playersTime = {}  # Use an empty dictionary to track players' total time
deathCounter = {}

death_messages = [
    'was shot by',
    'was pricked to death',
    'was stabbed to death',
    'was killed by',
    'was fireballed by',
    'was killed by magic',
    'was pummeled by',
    'was pricked to death',
    'drowned',
    'was burned to a crisp',
    'was burnt to a crisp',
    'was killed by magic',
    'blew up',
    'was blown up by',
    'was killed by magic',
    'was slain by',
    'was killed by magic',
    'was shot by a skull from',
    'was obliterated by a sonically-charged shriek',
    'froze to death',
    'was stung to death',
    'was shot by a skull from',
    'was impaled by',
    'was killed by magic',
    'was killed by',
    'fell out of the world',
    'fell from a high place',
    'hit the ground too hard',
    'was squashed by a falling anvil',
    'discovered the floor was lava',
    'suffocated in a wall',
    'was squished too much',
    'starved to death',
    'was impaled by',
    'withered away',
    'died from dehydration',
    'died',
    'was killed'
]

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

def getPlayersTime():
    with open(combined_file) as f:
        lines = f.readlines()
        print("___________PLAYERS TIME___________:")
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


def getDeathCounter():
    with open(combined_file) as f:
        lines = f.readlines()
        print("___________DEATHS___________:")
        for line in lines:
            if([word for word in death_messages if(word in line)] and 'Villager' not in line.split()[3]):
                username = (line.split(": ", 2)[1]).split()[0]
                deathCounter[username] = deathCounter.get(username, 0) + 1

    for key, value in sorted(deathCounter.items(), key=lambda item: item[1], reverse=True):
        print(key + ':', value)

def diamondsFoundRank():
    with open(combined_file) as f:
        lines = f.readlines()
        print("___________DIAMONDS FOUND___________:")
        for line in lines:
            if("[Diamonds!]" in line):
                username = (line.split(": ", 2)[1]).split()[0]
                print(username)
                
getPlayersTime()
getDeathCounter()
diamondsFoundRank()
