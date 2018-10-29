#!/usr/bin/env python
import argparse
import subprocess
import shlex
import os 
import sys

def add_command(tool, argument, description=None):
    if not os.path.exists(brief_path):
        os.makedirs(brief_path)
    with open(f"{brief_path}/{tool}.tool", "a") as myfile:
        myfile.write(f"{tool}|~|{argument}|~|{description}\n")

def remove_command(tool, line_number):
    with open(f"{brief_path}/{tool}.tool", "r") as infile:
        lines = infile.readlines()

    with open(f"{brief_path}/{tool}.tool", "w") as outfile:
        for pos, line in enumerate(lines):
            if pos != int(line_number) - 1:
                outfile.write(line)

def list_commands(tool):
    _, screen_width = os.popen('stty size', 'r').read().split()
    screen_width = int(screen_width)
    column_width = int(screen_width)//2

    print()
    print ('{0:<{2}}{1:<{2}}'.format("COMMAND", "    DESCRIPTION", column_width))
    print('-' * screen_width)
    with open(f"{brief_path}/{tool}.tool", "r") as myfile:
        counter = 1
        for line in myfile:
            argument = line.split("|~|")[1]
            description = line.split("|~|")[2]
            print ('{0}. {1:<{3}} {2:<{3}}'.format(counter, tool + " " + argument, description, column_width))
            counter += 1

brief_path = os.path.expanduser("~/.brief")
parser = argparse.ArgumentParser()
parser.add_argument("command", help="specify what argument to use, either add, ls or rm", nargs="*")
parser.add_argument("-d", "--description", help="description of command", const=True, default=False, nargs="?")
parser.add_argument("-t", "--tool", help="the name of the commandline tool", const=True, default=False, nargs="?")

args = parser.parse_args()
command = args.command[0] 
tool = args.command[1].split()[0]

if command == "add":
    argument = " ".join(args.command[1].split()[1:])
    if args.description != False:
        add_command(tool, argument, args.description)
    else:
        add_command(tool, argument)

if command == "ls":
    list_commands(tool)


if command == "rm":
    line_number = args.command[2]
    remove_command(tool, line_number)
