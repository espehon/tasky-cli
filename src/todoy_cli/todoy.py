

import os
import sys
import argparse
from configparser import ConfigParser

from colorama import Fore, init
init(autoreset=True)

parser = argparse.ArgumentParser()

# TODO: fix actions and nargs. All arguments can technically be passed 1 or more task integers (except --edit)
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


config_file = r"./src/todoy_cli/config.ini"
config = ConfigParser()

try:
    config.read(config_file)
except:
    print(f"{Fore.RED}FATAL: Reading config file failed!")
    sys.exit(1)


# data structure
data = {1:{
    'desc': 'This is a task',
    'status': 0, # 0: new, 1: started, 2: stopped, 3: complete, 4: delete
    'created': '2023-11-09',
    'switched': None, # date of last 
    'priority': 1, # 1,2,3,4
    'flag': False
}}


# unpack configs dict
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





def add_task():
    data_keys = data.keys()
    data_last_key = max(data_keys)

print(newTaskSymbol)

print("<<< EOF >>>")