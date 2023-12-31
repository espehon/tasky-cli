

import os
import sys
import argparse
import json
import datetime
from configparser import ConfigParser

from colorama import Fore, init
init(autoreset=True)

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--task', action='store_true', help='Add a new task')
parser.add_argument('-c', '--complete', nargs='+', metavar='T', action='store', type=int, help='Mark task(s) complete')
parser.add_argument('-s', '--switch', nargs='+', metavar='T', action='store', type=int, help='Toggle task(s) as started/stopped')
parser.add_argument('-f', '--flag', nargs='+', metavar='T', action='store', type=int, help='Flag task(s) with astrict (*)')
parser.add_argument('-p', '--priority', nargs=2, metavar=('T', 'P'), action='store', type=int, help='Set the priority of task [T] to [P]')
parser.add_argument('-e', '--edit', nargs=1,metavar='T', action='store', type=int, help='Enter edit mode on a task')
parser.add_argument('-d', '--delete', nargs='+', metavar='T', action='store', type=int, help='Mark task [T] for deletion')
parser.add_argument('--clear', action='store_true', help='Delete all resolved tasks and renumber')
parser.add_argument('text', nargs=argparse.REMAINDER, help='Task description')

args = parser.parse_args()

print(args)

data_file = r"./tasky.json"
config_file = r"./src/tasky_cli/config.ini"
config = ConfigParser()

try:
    config.read(config_file)
except:
    print(f"{Fore.RED}FATAL: Reading config file failed!")
    sys.exit(1)


# <<< data structure >>>
# data = {'1':{
#     'desc': 'This is a task',
#     'status': 0, # 0: new, 1: started, 2: stopped, 3: complete, 4: delete
#     'created': '2023-11-09',
#     'switched': None, # date of last status change
#     'priority': 1, # 1,2,3,4
#     'flag': False
# }}


# unpack configs dict
#TODO: #2 Nest each variable in a try/except to fall back to a default value if the user messed up the config file.
try:
    # variable_name = config["Settings"]["VarInFile"]
    newTaskSymbol = config["Settings"]["newTaskSymbol"]
    startedTaskSymbol = config["Settings"]["startedTaskSymbol"]
    stoppedTaskSymbol = config["Settings"]["stoppedTaskSymbol"]
    completeTaskSymbol = config["Settings"]["completeTaskSymbol"]

    newTaskColor = config["Settings"]["newTaskColor"]
    startedTaskColor = config["Settings"]["startedTaskColor"]
    stoppedTaskColor = config["Settings"]["stoppedTaskColor"]
    completeTaskColor = config["Settings"]["completeTaskColor"]

    priorityColor1 = config["Settings"]["priorityColor1"]
    priorityColor2 = config["Settings"]["priorityColor2"]
    priorityColor3 = config["Settings"]["priorityColor3"]
    priorityColor4 = config["Settings"]["priorityColor4"]

except:
    print(f"{Fore.RED}FATAL: Missing values in config file!")

with open(data_file, 'r') as json_file:
    data = json.load(json_file)

def index_data(current_dict: dict) -> list:
    output = []
    for k in current_dict.keys():
        output.append(int(k))
    return output

def build_new_task(index: int, task_desc: str, priority: bool, flagged: bool) -> dict:
    "Return new task as a dict for storage"
    output = {str(index): {
        "desc": task_desc,
        "status": 0,
        "created": str(datetime.datetime.now().date()),
        "switched": "None",
        "priority": priority,
        "flag": flagged
    }}
    return output






print(index_data(data))

print(newTaskSymbol)

print("<<< EOF >>>")
