#   Todo:
#   Load Option

import sys
import curses
from tabulate import tabulate
import csv
from datetime import datetime, timedelta
import os
import pyfiglet
from termcolor import colored
from colorama import init

menu_options = ['New File', 'Load File', 'Exit']

def print_menu(stdscr, selected_idx, menu_options):
    stdscr.clear() # Clears the screen
    h, w = stdscr.getmaxyx() # Get the height and width of the screen
    
    figlet = pyfiglet.Figlet(font = 'slant')
    
    title = figlet.renderText('2do2day')

    stdscr.addstr(title)

    for idx, option in enumerate(menu_options):
        x = w//2 - len(option)//2
        y = h//2 - len(menu_options)//2 + idx
        if idx == selected_idx:
            stdscr.addstr(y, x, option, curses.color_pair(1))
        else:
            stdscr.addstr(y,x, option)
    stdscr.refresh()

def main(stdscr):
    init()
    date_str = None
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_selected = 0
    curses.curs_set(0)
    print_menu(stdscr, current_selected, menu_options)

    while True:
        #   Gets user input
        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord('k')) and current_selected > 0:
            current_selected -= 1
        elif (key == curses.KEY_DOWN or key == ord('j')) and current_selected < len(menu_options) - 1:
            current_selected += 1
        elif (key == curses.KEY_ENTER or key == ord(' ')) or key in [10, 13]:
            stdscr.addstr(0,0, f"You selected '{menu_options[current_selected]}' Press ANY keys to continue ")
            stdscr.refresh()
            stdscr.getch()

            #   Here we check user's choice and go to related functions to the command

            if menu_options[current_selected] == 'Exit':
                sys.exit()
            elif menu_options[current_selected] == 'New File':
                stdscr.clear()
                Create(stdscr, None, False)
            elif menu_options[current_selected] == 'Load File':
                stdscr.clear()
                Loader(stdscr, date_str, 0)
        print_menu(stdscr, current_selected, menu_options)

def get_input(win, prompt_string):
    curses.echo()
    win.addstr(prompt_string)
    input_str = win.getstr().decode(encoding="utf-8")
    curses.noecho()
    return input_str

def get_task_number(filename):
    # Creates the CSV file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Number', 'Task', 'Time', 'Status'])
            writer.writeheader()

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        task_numbers = [int(row['Number']) for row in reader]
    if not task_numbers:
        return 1
    return max(task_numbers) + 1

def Create(stdscr, date_str, fromLoad):
    stdscr.clear() # Clears the screen
    if date_str == None:
        date_str = get_input(stdscr, 'File Name: ')
    else:
        pass
    if fromLoad:
        filename = f'{date_str}'
    else:
        filename = f'{date_str}.csv'
    tasks = []
    status = 'Not Started'
    i = 1

    # Asks for input
    task = get_input(stdscr, 'Task: ')
    time = get_input(stdscr, 'Time: ')
    task_number = get_task_number(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Number', 'Task', 'Time', 'Status'])
        if file.tell() == 0:  # If file is empty, write headers
            writer.writeheader()
        writer.writerow({'Number': task_number, 'Task': task, 'Time': time, 'Status': status})

    # Reload and show tasks after creating the new task
    stdscr.clear()
    view(stdscr, filename)
#        reader = csv.DictReader(file)
#        tasks = [row for row in reader]
#    stdscr.addstr(tabulate(tasks, headers='keys', tablefmt='rounded_outline'))  # Displaying using tabulate
#    stdscr.refresh()
#    stdscr.getch()

def Loader(stdscr, date_str, current_selected):

    dir = os.listdir('./')
    dirList = []
    for file in dir:
        if str(file).endswith('.csv'):
            dirList.append(file)

    print_menu(stdscr, current_selected, dirList)

    while True:
        #   Gets user input
        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord('k')) and current_selected > 0:
            current_selected -= 1
        elif (key == curses.KEY_DOWN or key == ord('j')) and current_selected < len(dirList) - 1:
            current_selected += 1
        elif key == ord('b'):
            main(stdscr)
        elif key == ord('d'):
            stdscr.clear()
            dirList.remove(dirList[current_selected])
            os.remove('./' + dirList[current_selected])
            stdscr.addstr(0, 0, f'{dirList[current_selected]} Got Deleted.')
        elif (key == curses.KEY_ENTER or key == ord(' ')) or key in [10, 13]:
            stdscr.addstr(0,0, f"You selected '{dirList[current_selected]}' Press ANY keys to continue ")
            stdscr.refresh()
            stdscr.getch()
            date_str = str(dirList[current_selected])
            view(stdscr, date_str)
        print_menu(stdscr, current_selected, dirList)


def view(stdscr, date_str):

    stdscr.clear() # Clears the screen
    filename = date_str
    if not os.path.exists(filename):
        Create(stdscr, date_str, False)
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        tasks = [row for row in reader]
    stdscr.addstr('\n\n' + tabulate(tasks, headers='keys', tablefmt='rounded_outline')
        + '\n\n [i]nsert | [e]dit | [d]elete | [m]ark completed | [b]ack')  # Displaying using tabulate
    stdscr.refresh()
    stdscr.getch()

    while True:
        c = stdscr.getch()
        if c == ord('i'):
            stdscr.clear()
            Create(stdscr, date_str, True)
        if c == ord('e'):
            stdscr.clear()
            edit(stdscr, date_str)
        if c == ord('d'):
            stdscr.clear()
            delete(stdscr, date_str)
        if c == ord('m'):
            stdscr.clear()
            mark(stdscr, date_str)
        if c == ord('b'):
            stdscr.clear()
            main(stdscr)

def delete(stdscr, date_str):
    stdscr.clear()
    task_to_remove = get_input(stdscr, 'Number of Task to Remove: ')
    new_tasks = []

    filename = f'{date_str}'

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Number'] != task_to_remove:
                new_tasks.append(row)

    for idx, task in enumerate(new_tasks, start=1):
        task['Number'] = idx

    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Number', 'Task', 'Time', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_tasks)

    stdscr.clear()
    view(stdscr, date_str)


def edit(stdscr, date_str):
    stdscr.clear()
    task_to_edit = get_input(stdscr, 'Number of Task to Edit: ')
    edit_to_what = get_input(stdscr, 'Change it to: ')
    new_tasks = []

    filename = f'{date_str}'

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Number'] == task_to_edit:
                row['Task'] = edit_to_what
            new_tasks.append(row)

    for idx, task in enumerate(new_tasks, start=1):
        task['Number'] = idx

    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Number', 'Task', 'Time', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_tasks)

    stdscr.clear()
    view(stdscr, date_str)

def mark(stdscr, date_str):
    filename = f'{date_str}'
    stdscr.clear()
    task_to_mark = get_input(stdscr, 'Number of Task You Completed: ')
    new_tasks = []

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Number'] == task_to_mark:
                row['Status'] = 'Completed'
            new_tasks.append(row)

    for idx, task in enumerate(new_tasks, start=1):
        task['Number'] = idx

    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Number', 'Task', 'Time', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_tasks)

    stdscr.clear()
    view(stdscr, date_str)

if __name__ == "__main__":
    curses.wrapper(main)
