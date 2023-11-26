


import argparse

parser = argparse.ArgumentParser()

# TODO: fix actions and nargs. All arguments can technically be passed 1 or more task integers (except --edit)
parser.add_argument('-t', '--task', action='store_true', help='Add a new task')
parser.add_argument('-c', '--complete', nargs='+', action='store', type=int, help='Mark task(s) complete')
parser.add_argument('-s', '--switch', nargs='+', action='store', type=int, help='Toggle task(s) as started/stopped')
parser.add_argument('-f', '--flag', nargs='+', action='store', type=int, help='Flag task(s) with astrict (*)')
parser.add_argument('-p', '--priority', nargs=2, action='store', type=int, help='Set the priority of task [T] to [P]')
parser.add_argument('-e', '--edit', nargs=1, action='store', type=int, help='Enter edit mode on a task')
parser.add_argument('-d', '--delete', nargs='+', action='store', type=int, help='Mark task [T] for deletion')
parser.add_argument('--clear', action='store_true', help='Delete all resolved tasks and renumber')
parser.add_argument('text', nargs=argparse.REMAINDER, help='Task description')

args = parser.parse_known_args(['--clear', '1', 'hello'])

print(args)


# data structure
data = {1:{
    'desc': 'This is a task',
    'status': 0, # 0: new, 1: started, 2: stopped, 3: complete, 4: delete
    'created': '2023-11-09',
    'switched': None,
    'priority': 0, # 0,1,2,3
    'flag': False
}}

print("<<< EOF >>>")