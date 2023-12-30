


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--task', action='store_true', help='Add a new task')
parser.add_argument('text', nargs=argparse.REMAINDER, help='Task description')

args = parser.parse_known_args(['-t', 'hello', 'world!'])

print(args)
