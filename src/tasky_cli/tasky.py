

import os
import sys
import argparse
import json
import datetime
import copy
from configparser import ConfigParser

from colorama import Fore, Style, init
init(autoreset=True)

# Set user paths
home = os.path.expanduser("~")
config_path = os.path.expanduser("~/.config/tasky/")
config_file = f"{config_path}tasky.ini"

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

# args = parser.parse_args()


config = ConfigParser()

PRIORITIES = (1, 2, 3, 4)
DEFAULT_PRIORITY = 1

DEFAULT_CONFIGS = """\
[Settings]
taskPath = "~/.local/share/tasky/"
taskFile = "tasky.json"

newTaskSymbol = "[!]"
startedTaskSymbol = "[>]"
stoppedTaskSymbol = "[.]"
completeTaskSymbol = " √ "
flagSymbol = "🏳"

boarderColor = "bright_black"
newTaskColor = "red"
startedTaskColor = "bright_yellow"
stoppedTaskColor = "bright_red"
completeTaskColor = "bright_green"

priorityColor1 = "white"
priorityColor2 = "cyan"
priorityColor3 = "yellow"
priorityColor4 = "red"

prioritySymbol1 = ""
prioritySymbol2 = "(!)"
prioritySymbol3 = "(!!)"
prioritySymbol4 = "(!!!)"
"""

# if path does not exist, create it.
if os.path.exists(config_path) == False:
    os.makedirs(config_path)

# if file does not exist, create it.
if os.path.exists(config_file) == False:
    with open(config_file, 'w', encoding='utf-8') as settingsFile:
        settingsFile.write(DEFAULT_CONFIGS)


try:
    config.read(config_file, encoding='utf-8')
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

colors = {
    'red': {'norm': Fore.RED, 'alt': Fore.LIGHTRED_EX},
    'yellow': {'norm': Fore.YELLOW, 'alt': Fore.LIGHTYELLOW_EX},
    'green': {'norm': Fore.GREEN, 'alt': Fore.LIGHTGREEN_EX},
    'cyan': {'norm': Fore.CYAN, 'alt': Fore.LIGHTCYAN_EX},
    'blue': {'norm': Fore.BLUE, 'alt': Fore.LIGHTBLUE_EX},
    'magenta': {'norm': Fore.MAGENTA, 'alt': Fore.LIGHTMAGENTA_EX},
    'black': {'norm': Fore.BLACK, 'alt': Fore.LIGHTBLACK_EX},
    'white': {'norm': Fore.WHITE, 'alt': Fore.LIGHTWHITE_EX},

    'bright_red': {'norm': Fore.LIGHTRED_EX, 'alt': Fore.RED},
    'bright_yellow': {'norm': Fore.LIGHTYELLOW_EX, 'alt': Fore.YELLOW},
    'bright_green': {'norm': Fore.LIGHTGREEN_EX, 'alt': Fore.GREEN},
    'bright_cyan': {'norm': Fore.LIGHTCYAN_EX, 'alt': Fore.CYAN},
    'bright_blue': {'norm': Fore.LIGHTBLUE_EX, 'alt': Fore.BLUE},
    'bright_magenta': {'norm': Fore.LIGHTMAGENTA_EX, 'alt': Fore.MAGENTA},
    'bright_black': {'norm': Fore.LIGHTBLACK_EX, 'alt': Fore.BLACK},
    'bright_white': {'norm': Fore.LIGHTWHITE_EX, 'alt': Fore.WHITE},
}


# unpack configs dict
#TODO: #2 Nest each variable in a try/except to fall back to a default value if the user messed up the config file.
try:
    # variable_name = config["Settings"]["VarInFile"]
    data_path = config["Settings"]["taskPath"].replace('\"', '')
    data_file = config["Settings"]["taskFile"].replace('\"', '')

    newTaskSymbol = config["Settings"]["newTaskSymbol"].replace('\"', '')
    startedTaskSymbol = config["Settings"]["startedTaskSymbol"].replace('\"', '')
    stoppedTaskSymbol = config["Settings"]["stoppedTaskSymbol"].replace('\"', '')
    completeTaskSymbol = config["Settings"]["completeTaskSymbol"].replace('\"', '')
    flagSymbol = config["Settings"]["flagSymbol"].replace('\"', '')

    boarderColor = config['Settings']['boarderColor'].replace('\"', '')
    newTaskColor = config["Settings"]["newTaskColor"].replace('\"', '')
    startedTaskColor = config["Settings"]["startedTaskColor"].replace('\"', '')
    stoppedTaskColor = config["Settings"]["stoppedTaskColor"].replace('\"', '')
    completeTaskColor = config["Settings"]["completeTaskColor"].replace('\"', '')

    priorityColor1 = config["Settings"]["priorityColor1"].replace('\"', '')
    priorityColor2 = config["Settings"]["priorityColor2"].replace('\"', '')
    priorityColor3 = config["Settings"]["priorityColor3"].replace('\"', '')
    priorityColor4 = config["Settings"]["priorityColor4"].replace('\"', '')

    prioritySymbol1 = config["Settings"]["prioritySymbol1"].replace('\"', '')
    prioritySymbol2 = config["Settings"]["prioritySymbol2"].replace('\"', '')
    prioritySymbol3 = config["Settings"]["prioritySymbol3"].replace('\"', '')
    prioritySymbol4 = config["Settings"]["prioritySymbol4"].replace('\"', '')


except Exception as e:
    print(f"{Fore.RED}{e}")

priority_color = {
    1: priorityColor1,
    2: priorityColor2,
    3: priorityColor3,
    4: priorityColor4,
}

priority_symbol = {
    1: prioritySymbol1,
    2: prioritySymbol2,
    3: prioritySymbol3,
    4: prioritySymbol4,
}

# if path does not exist, create it.
data_path = os.path.expanduser(data_path)
if os.path.exists(data_path) == False:
    os.makedirs(data_path)

data_path_file = data_path + data_file

# if file does not exist, create it.
if os.path.exists(data_path_file) == False:
    with open(data_path_file, 'w') as json_file:
        data = {}
        json.dump(data, json_file, indent=4)

with open(data_path_file, 'r') as json_file:
    data = json.load(json_file)

def update_tasks():
    """Write data dict to json"""
    with open(data_path_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def color(color_name: str, alternate_style: bool=False) -> str:
    key1 = color_name
    key2 = 'norm' if not alternate_style else 'alt'
    return colors[key1][key2]

def color_gradient(scale: int) -> str:
    """Takes a float between 0 and 100 inclusive and returns a colorama color"""
    if scale >= 100:
        return Fore.LIGHTWHITE_EX
    elif scale >= 87:
        return Fore.LIGHTCYAN_EX
    elif scale >= 75:
        return Fore.CYAN
    elif scale >= 62:
        return Fore.LIGHTGREEN_EX
    elif scale >= 50:
        return Fore.GREEN
    elif scale >= 37:
        return Fore.LIGHTYELLOW_EX
    elif scale >= 25:
        return Fore.YELLOW
    elif scale >= 12:
        return Fore.LIGHTRED_EX
    else:
        return Fore.RED

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
    data_copy = copy.deepcopy(data)
    done, working, pending = 0, 0, 0
    for key, task in data.items():
        status = task['status']
        if status in [0, 2]:
            pending += 1
        elif status in [1]:
            working += 1
        elif status in [3]:
            done += 1
        elif status in [4]:
            data_copy.pop(key)
    total = done + working + pending
    rate = int((done / total) * 100)
    desc_lens = []
    for task in data_copy.values():
        desc_lens.append(len(task['desc']))
    buffer = 20
    width = max(desc_lens) + buffer
    header = ("\n"*4) + "❮❮❮ tasky ❯❯❯".center(int(width*0.8)) + "\n"
    boarder = [color(boarderColor) + "┍" + ("━"*width),
                " " + (color(boarderColor) + "─"*width) + "┚"]
    title = f"{color(boarderColor)}│{Style.RESET_ALL}  Tasks {color(boarderColor)}[{done}/{total}]"
    complete_stat = f"{color_gradient(rate)}{str(rate).rjust(3)}%{color(boarderColor)} of all tasks complete.{Style.RESET_ALL}"
    breakdown_stat = f"{color(completeTaskColor)}{str(done).rjust(3)}{color(boarderColor)} done · {color(startedTaskColor)}{working}{color(boarderColor)} in-progress · {color(stoppedTaskColor)}{pending}{color(boarderColor)} pending"
    def get_task_lines():
        for key, task in data_copy.items():
            if task['flag']:
                flag = flagSymbol
            else:
                flag = ""
            id = f"{flag.rjust(2)}{color(boarderColor) + key.rjust(3) + '. ' + Style.RESET_ALL}"
            if task['status'] == 0:
                symbol = color(newTaskColor) + newTaskSymbol + Style.RESET_ALL + "  "
            elif task['status'] == 1:
                symbol = color(startedTaskColor) + startedTaskSymbol + Style.RESET_ALL + "  "
            elif task['status'] == 2:
                symbol = color(stoppedTaskColor) + stoppedTaskSymbol + Style.RESET_ALL + "  "
            elif task['status'] == 3:
                symbol = color(completeTaskColor) + completeTaskSymbol + Style.RESET_ALL + "  "
            
            if task['status'] == 3:
                desc = color(boarderColor) + task['desc'] + " " + priority_symbol[task['priority']] + Style.RESET_ALL + " "
            else:
                desc = color(priority_color[task['priority']], task['flag']) + task['desc'] + " " + priority_symbol[task['priority']] + Style.RESET_ALL + " "
            
            if task['status'] in [3]:
                start_date = datetime.datetime.strptime(task['created'], "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(task['switched'], "%Y-%m-%d").date()
            else:
                start_date = datetime.datetime.strptime(task['created'], "%Y-%m-%d").date()
                end_date = datetime.datetime.now().date()
            delta = end_date - start_date
            days = f"{color(boarderColor)}{str(delta.days)}d{Style.RESET_ALL}"
            
            print(id + symbol + desc + days)

    print(header)
    if prolog != "":
        print(f"{prolog}\n")
    print(boarder[0])
    print(title)
    get_task_lines()
    print(boarder[1])
    print(complete_stat)
    print(breakdown_stat)



# Main
def tasky(argv=None):
    args = parser.parse_args(argv) #Execute parse_args()

    tasks_index = index_data(data)
    next_index = max(tasks_index) + 1
    passed_string = (" ".join(args.text)).strip()
    passed_priority = check_for_priority(passed_string[-3:])

    if passed_priority[0]:
        passed_string = passed_string[:-3].strip()

    # --task
    if args.task:    
        new_task = format_new_task(next_index, passed_string, passed_priority[1], False)
        data.update(new_task)
        update_tasks()
        render_tasks("New task added.")

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
            render_tasks(f"{updates} task{'' if updates == 1 else 's'} updated.")

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
            render_tasks(f"{updates} task{'' if updates == 1 else 's'} updated.")

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
            render_tasks(f"{updates} task{'' if updates == 1 else 's'} marked for deletion.")

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
            render_tasks("Tasks cleaned.")

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
                render_tasks(f"Task #{T} set to priority level {P}.")
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
            render_tasks(f"{updates} task{'' if updates == 1 else 's'} updated.")

    # --edit
    elif args.edit:
        task_key = str(args.edit[0])
        if task_key in data:
            new_desc = input(f"Enter new task description for #{task_key}...\n>>> ").strip()
            data[task_key]['desc'] = new_desc
            update_tasks()
            render_tasks(f"Task #{task_key} has been edited.")
        else:
            print(f"\t'{task_key}' is an invalid task id.")

    # no args
    else:
        render_tasks()
    



