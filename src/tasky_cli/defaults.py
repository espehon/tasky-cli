# Copyright (c) 2024 espehon
# MIT License

import sys


if sys.stdout.encoding.lower() == 'utf-8':
    style = 'fancy'
else:
    style = 'plain'


DEFAULT_CHARS = {
    'newTaskSymbol': {
        'fancy': '[!]',
        'plain': '[!]'
    },
    'startedTaskSymbol': {
        'fancy': '[▶]',
        'plain': '[>]'
    },
    'stoppedTaskSymbol': {
        'fancy': '[.]',
        'plain': '[.]'
    },
    'completeTaskSymbol': {
        'fancy': '✔ ',
        'plain': '√ '
    },
    'flagSymbol': {
        'fancy': '🏳 ',
        'plain': ' *'
    },
    'flagSymbolAlt': {
        'fancy': '🏴',
        'plain': ' *'
    },
    'prioritySymbol1': {
        'fancy': '',
        'plain': ''
    },
    'prioritySymbol2': {
        'fancy': '(!)',
        'plain': '(!)'
    },
    'prioritySymbol3': {
        'fancy': '(!!)',
        'plain': '(!!)'
    },
    'prioritySymbol4': {
        'fancy': '(!!!)',
        'plain': '(!!!)'
    }
}


default_configs = f"""\
[Settings]
taskPath = "~/.local/share/tasky/"
taskFile = "tasky.json"

newTaskSymbol = "{DEFAULT_CHARS['newTaskSymbol'][style]}"
startedTaskSymbol = "{DEFAULT_CHARS['startedTaskSymbol'][style]}"
stoppedTaskSymbol = "{DEFAULT_CHARS['stoppedTaskSymbol'][style]}"
completeTaskSymbol = "{DEFAULT_CHARS['completeTaskSymbol'][style]}"
flagSymbol = "{DEFAULT_CHARS['flagSymbol'][style]}"
flagSymbolAlt = "{DEFAULT_CHARS['flagSymbolAlt'][style]}"

boarderColor = "bright_black"
newTaskColor = "red"
startedTaskColor = "bright_yellow"
stoppedTaskColor = "bright_red"
completeTaskColor = "bright_green"

priorityColor1 = "white"
priorityColor2 = "cyan"
priorityColor3 = "yellow"
priorityColor4 = "red"

prioritySymbol1 = "{DEFAULT_CHARS['prioritySymbol1'][style]}"
prioritySymbol2 = "{DEFAULT_CHARS['prioritySymbol2'][style]}"
prioritySymbol3 = "{DEFAULT_CHARS['prioritySymbol3'][style]}"
prioritySymbol4 = "{DEFAULT_CHARS['prioritySymbol4'][style]}"
"""