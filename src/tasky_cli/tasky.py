

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
parser.add_argument('-e', '--edit', nargs=1, metavar='T', action='store', type=int, help='Enter edit mode on a task')
parser.add_argument('-d', '--delete', nargs='+', metavar='T', action='store', type=int, help='Mark task [T] for deletion')
parser.add_argument('--clean', action='store_true', help='Remove complete/deleted tasks and reset indices')
parser.add_argument('text', nargs=argparse.REMAINDER, help='Task description')

args = parser.parse_args()

print(args)

data_file = r"./tasky.json"
config_file = r"./src/tasky_cli/config.ini"
config = ConfigParser()

PRIORITIES = (1, 2, 3, 4)
DEFAULT_PRIORITY = 1

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

def update_tasks():
    """Write data dict to json"""
    with open(data_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def index_data(current_dict: dict) -> list:
    """
    Return list of keys as int from data dict.
    This is to get around the JavaScript limitation of keys being strings
    """
    output = []
    for k in current_dict.keys():
        output.append(int(k))
    return output

def format_new_task(index: int, task_desc: str, priority: int, flagged: bool) -> dict:
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

def check_for_priority(text: str) -> tuple:
    """
    Returns a tuple containing bool and int.
    Bool represents if the priority was passed in the task description.
    Int represents the priority.
    """
    # This could be done with a match/case block, but I want to keep the Python requirements low.
    if len(text) == 3:
        a, b, c = text
        if str.lower(a) == 'p':
            if b == ':':
                try:
                    if int(c) in PRIORITIES:
                        return (True, int(c))
                except:
                    pass
    return (False, DEFAULT_PRIORITY)

def render_tasks(prolog: str="") -> None:
    #TODO finally, the fun part!
    desc_lens = []
    for task in data.values():
        desc_lens.append(len(task['desc']))
    width = max(desc_lens)





tasks_index = index_data(data)
next_index = max(tasks_index) + 1
passed_string = (" ".join(args.text)).strip()
passed_priority = check_for_priority(passed_string[-3:])

if passed_priority[0]:
    passed_string = passed_string[:-3].strip()




print("-----")

# Main

# --task
if args.task:    
    new_task = format_new_task(next_index, passed_string, passed_priority[1], False)
    data.update(new_task)
    update_tasks()
    print("\tNew task added.")

# --switch
elif args.switch:
    updates = 0
    task_keys = [str(i) for i in args.switch]
    for task_key in task_keys:
        working_task = data[task_key]
        new_status = None
        if working_task['status'] in [0, 2]:
            new_status = 1
        elif working_task['status'] in [1]:
            new_status = 2
        if new_status is not None:
            working_task['status'] = new_status
            working_task['switched'] = str(datetime.datetime.now().date())
            data[task_key] = working_task
            updates += 1
    if updates > 0:
        update_tasks()
        print(f"\t{updates} task{'' if updates == 1 else 's'} updated.")

# --complete
elif args.complete:
    updates = 0
    task_keys = [str(i) for i in args.complete]
    for task_key in task_keys:
        working_task = data[task_key]
        new_status = None
        if working_task['status'] in [0, 1, 2]:
            new_status = 3
        elif working_task['status'] in [3]:
            new_status = 1
        if new_status is not None:
            working_task['status'] = new_status
            working_task['switched'] = str(datetime.datetime.now().date())
            data[task_key] = working_task
            updates += 1
    if updates > 0:
        update_tasks()
        print(f"\t{updates} task{'' if updates == 1 else 's'} updated.")

# --delete
elif args.delete:
    updates = 0
    task_keys = [str(i) for i in args.delete]
    for task_key in task_keys:
        working_task = data[task_key]
        new_status = None
        if working_task['status'] != 4:
            new_status = 4
        if new_status is not None:
            working_task['status'] = new_status
            working_task['switched'] = str(datetime.datetime.now().date())
            data[task_key] = working_task
            updates += 1
    if updates > 0:
        update_tasks()
        print(f"\t{updates} task{'' if updates == 1 else 's'} marked for deletion.")

# --clear
elif args.clean:
    updates = 0
    task_keys = [str(i) for i in tasks_index]
    for key in task_keys:
        if data[key]['status'] in [3, 4]:
            data.pop(key)
            updates += 1
    new_data = {}
    for index, task in enumerate(data.values()):
        new_data[str(index + 1)] = task
    data = new_data
    update_tasks()
    if updates > 0:
        print("\tTasks cleaned.")

# --priority
elif args.priority:
    updates = 0
    T, P = args.priority
    if P in PRIORITIES:
        if data[str(T)]['priority'] != P:
            data[str(T)]['priority'] = P
            updates += 1
        if updates > 0:
            update_tasks()
            print(f"\tTask #{T} set to priority level {P}.")
    else:
        print(f"\t{P} is not an available priority level.")

# --flag
elif args.flag:
    updates = 0
    task_keys = [str(i) for i in args.flag]
    for task_key in task_keys:
        try:
            working_task = data[task_key]
            working_task['flag'] = not working_task['flag']
            updates += 1
        except:
            print(f"\t'{task_key}' is an invalid task id.")
    if updates > 0:
        update_tasks()
        print(f"\t{updates} task{'' if updates == 1 else 's'} updated.")

# --edit
elif args.edit:
    task_key = str(args.edit[0])
    if task_key in data:
        new_desc = input(f"Enter new task description for #{task_key}...\n>>> ").strip()
        data[task_key]['desc'] = new_desc
        update_tasks()
        print(f"\tTask #{task_key} has been edited.")
    else:
        print(f"\t'{task_key}' is an invalid task id.")

    



