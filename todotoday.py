from os.path import isdir, isfile
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
    stdscr.clear()  # Clears the screen
    h, w = stdscr.getmaxyx()  # Get the height and width of the screen
    
    figlet = pyfiglet.Figlet(font='slant')
    
    title = figlet.renderText('2do2day')
    
    # Use a color pair for the title
    stdscr.addstr(title, curses.color_pair(2))  

    stdscr.addstr('\n[j]up | [k]down | [d]elete | [b]ack')

    for idx, option in enumerate(menu_options):
        x = w // 2 - len(option) // 2
        y = h // 2 - len(menu_options) // 2 + idx
        if idx == selected_idx:
            stdscr.addstr(y, x, option, curses.color_pair(1))  # Highlighted selection
        else:
            stdscr.addstr(y, x, option, curses.color_pair(3))  # Unselected option
    stdscr.refresh()

def main(stdscr):
    init()
    date_str = None

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Selected item
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Title color
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Unselected item
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Instructions 

    current_selected = 0
    curses.curs_set(0)
    print_menu(stdscr, current_selected, menu_options)

    while True:
        # Gets user input
        key = stdscr.getch()

        if (key == curses.KEY_UP or key == ord('k')) and current_selected > 0:
            current_selected -= 1
        elif (key == curses.KEY_DOWN or key == ord('j')) and current_selected < len(menu_options) - 1:
            current_selected += 1
        elif (key == curses.KEY_ENTER or key == ord(' ')) or key in [10, 13]:
            stdscr.addstr(0, 0, f"You selected '{menu_options[current_selected]}' Press ANY key to continue ")
            stdscr.refresh()
            stdscr.getch()

            # Check user's choice
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
    stdscr.clear()
    if date_str is None:
        date_str = get_input(stdscr, 'File Name: ')
    if fromLoad:
        filename = date_str
    else:
        if not isdir('./csvs/'):
            os.mkdir('./csvs/')
        filename = f'{date_str}.csv'
        filename = os.path.join('./csvs/', filename)

    # filename = date_str
    tasks = []
    status = 'Not Started'
    i = 1

    task = get_input(stdscr, 'Task: ')
    time = get_input(stdscr, 'Time: ')
    task_number = get_task_number(filename)
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Number', 'Task', 'Time', 'Status'])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({'Number': task_number, 'Task': task, 'Time': time, 'Status': status})
    except IOError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error: {str(e)}")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    view(stdscr, filename)

def Loader(stdscr, date_str, current_selected):
    if not os.path.isdir('./csvs/'):
        os.mkdir('./csvs/')
    dir = os.listdir('./csvs/')
    dirList = [file for file in dir if file.endswith('.csv')]
    if not dirList:
        dirList = ['empty']

    print_menu(stdscr, current_selected, dirList)

    while True:
        key = stdscr.getch()
        
        if key == ord('b'):
            main(stdscr)
        if dirList[0] != 'empty':
            if (key == curses.KEY_UP or key == ord('k')) and current_selected > 0:
                current_selected -= 1
            elif (key == curses.KEY_DOWN or key == ord('j')) and current_selected < len(dirList) - 1:
                current_selected += 1
            elif key == ord('d'):
                file_to_delete = os.path.join('./csvs/', dirList[current_selected])
                try:
                    os.remove(file_to_delete)
                    dirList.pop(current_selected)
                    if not dirList:
                        dirList = ['empty']
                    current_selected = min(current_selected, len(dirList) - 1)
                    stdscr.clear()
                    stdscr.addstr(0, 0, f'{os.path.basename(file_to_delete)} has been deleted.')
                except OSError as e:
                    stdscr.clear()
                    stdscr.addstr(0, 0, f"Error deleting file: {str(e)}")
                stdscr.refresh()
                stdscr.getch()
            elif (key == curses.KEY_ENTER or key == ord(' ')) or key in [10, 13]:
                stdscr.addstr(0, 0, f"You selected '{dirList[current_selected]}' Press ANY key to continue ")
                stdscr.refresh()
                stdscr.getch()
                date_str = str(dirList[current_selected])
                view(stdscr, os.path.join('./csvs/', date_str))
        print_menu(stdscr, current_selected, dirList)

def view(stdscr, date_str):
    stdscr.clear()
    filename = date_str
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            tasks = [row for row in reader]
        stdscr.addstr('\n\n' + tabulate(tasks, headers='keys', tablefmt='rounded_outline'))
        stdscr.addstr('\n\n [i]nsert | [e]dit | [t]ime edit | [d]elete \n\n [c]lear | [m]ark completed | [s]wap | [b]ack', curses.color_pair(4))
    except IOError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error: {str(e)}")
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
        if c == ord('t'):
            stdscr.clear()
            editTime(stdscr, date_str)
        if c == ord('d'):
            stdscr.clear()
            delete(stdscr, date_str)
        if c == ord('m'):
            stdscr.clear()
            mark(stdscr, date_str)
        if c == ord('b'):
            stdscr.clear()
            main(stdscr)
        if c == ord('s'):
            stdscr.clear()
            swap(stdscr, date_str)
        if c == ord('c'):
            stdscr.clear()
            clear(stdscr, date_str)

def delete(stdscr, date_str):
    stdscr.clear()
    task_to_remove = get_input(stdscr, 'Number of Task to Remove: ')
    new_tasks = []

    # filename = os.path.join('./csvs/', date_str)
    filename = date_str

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Number'] != task_to_remove:
                    new_tasks.append(row)
    except IOError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error: {str(e)}")
        stdscr.refresh()
        stdscr.getch()
        return

    for idx, task in enumerate(new_tasks):
        task['Number'] = idx + 1  # Re-number tasks

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Number', 'Task', 'Time', 'Status'])
        writer.writeheader()
        writer.writerows(new_tasks)

    view(stdscr, date_str)

def swap(stdscr, date_str):
    stdscr.clear()
    task_number = get_input(stdscr, 'Task1: ')
    other_task_number = get_input(stdscr, 'Task2: ')
    new_tasks = []

    # filename =os.path.join('./csvs/', date_str)
    filename = date_str

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            other = None
            temp = None

            for row in reader:
                if row['Number'] == other_task_number:
                    other = row
                if row['Number'] == task_number:
                    temp = row
                new_tasks.append(row)

            for i, row in enumerate(new_tasks):
                task_number = int(task_number)
                other_task_number = int(other_task_number)
                if i == task_number - 1:
                    new_tasks[i] = other
                    new_tasks[i]['Number'] = i + 1
                elif i == other_task_number - 1:
                    new_tasks[i] = temp 
                    new_tasks[i]['Number'] = i + 1


    except IOError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error: {str(e)}")
        stdscr.refresh()
        stdscr.getch()
        return

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Number', 'Task', 'Time', 'Status'])
        writer.writeheader()
        writer.writerows(new_tasks)

    view(stdscr, date_str)

def edit(stdscr, date_str):
    stdscr.clear()
    task_number = get_input(stdscr, 'Number of Task to Edit: ')
    new_task = get_input(stdscr, 'New Task: ')
    new_tasks = []

    # filename =os.path.join('./csvs/', date_str)
    filename = date_str

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Number'] == task_number:
                    row['Task'] = new_task
                new_tasks.append(row)
    except IOError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error: {str(e)}")
        stdscr.refresh()
        stdscr.getch()
        return

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Number', 'Task', 'Time', 'Status'])
        writer.writeheader()
        writer.writerows(new_tasks)

    view(stdscr, date_str)

def editTime(stdscr, date_str):
    stdscr.clear()
    task_number = get_input(stdscr, 'Number of Task to Edit Time: ')
    new_time = get_input(stdscr, 'New Time: ')
    new_tasks = []

    filename = date_str

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Number'] == task_number:
                    row['Time'] = new_time
                new_tasks.append(row)
    except IOError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error: {str(e)}")
        stdscr.refresh()
        stdscr.getch()
        return

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Number', 'Task', 'Time', 'Status'])
        writer.writeheader()
        writer.writerows(new_tasks)

    view(stdscr, date_str)

def mark(stdscr, date_str):
    stdscr.clear()
    task_number = get_input(stdscr, 'Number of Task to Mark Completed: ')
    new_tasks = []

    # filename = os.path.join('./csvs/', date_str)

    filename = date_str

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Number'] == task_number:
                    row['Status'] = 'Completed'
                new_tasks.append(row)
    except IOError as e:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Error: {str(e)}")
        stdscr.refresh()
        stdscr.getch()
        return

    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Number', 'Task', 'Time', 'Status'])
        writer.writeheader()
        writer.writerows(new_tasks)

    view(stdscr, date_str)


def clear(stdscr, date_str):
    stdscr.clear()
    answer = get_input(stdscr, 'Clear all: Are You sure? [y/n] ')
    new_tasks = []

    # filename =os.path.join('./csvs/', date_str)
    filename = date_str

    if answer == 'y':
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Number', 'Task', 'Time', 'Status'])
            writer.writeheader()
            writer.writerows(new_tasks)

    view(stdscr, date_str)

curses.wrapper(main)
