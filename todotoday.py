import curses
from tabulate import tabulate
import csv
from datetime import datetime
import os

#   Here are the menu options as a list:
menu_options = ["View Today's Todolist", 'Add a Task', 'Edit a Task', 'Delete a Task', 'Mark Task as Complete', 'Exit']

#   Here we define the function that displays the menu:
def print_menu(stdscr, selected_idx):
    stdscr.clear() # Clears the screen
    h, w = stdscr.getmaxyx() # Get the height and width of the screen

    for idx, option in enumerate(menu_options):
        x = w//2 - len(option)//2
        y = h//2 - len(menu_options)//2 + idx
        if idx == selected_idx:
            stdscr.addstr(y, x, option, curses.color_pair(1))
        else:
            stdscr.addstr(y,x, option)
    stdscr.refresh()

def main(stdscr):
    #   Here we set up color for selected option
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    #   Here we make program to start with the first option selected
    current_selected = 0
    #   Here we hide the cursor
    curses.curs_set(0)
    #   Prints the current menu
    print_menu(stdscr, current_selected)

    while True:
        #   Gets user input
        key = stdscr.getch()

        if key == curses.KEY_UP and current_selected > 0:
            current_selected -= 1
        elif key == curses.KEY_DOWN and current_selected < len(menu_options) - 1:
            current_selected += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.addstr(0,0, f"You selected '{menu_options[current_selected]}' Press ANY keys to continue ")
            stdscr.refresh()
            stdscr.getch()

            #   Here we check user's choice and go to related functions to the command

            if menu_options[current_selected] == 'Exit':
                break
            elif menu_options[current_selected] == 'Add a Task':
                stdscr.clear()
                create(stdscr)
            elif menu_options[current_selected] == "View Today's Todolist":
                stdscr.clear()
                view(stdscr)
            elif menu_options[current_selected] == 'Delete a Task':
                stdscr.clear()
                delete(stdscr)
            elif menu_options[current_selected] == 'Edit a Task':
                stdscr.clear()
                edit(stdscr)
            elif menu_options[current_selected] == 'Mark Task as Complete':
                stdscr.clear()
                mark(stdscr)
        print_menu(stdscr, current_selected)

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

def create(stdscr):
    date_str = datetime.now().strftime("%Y-%m-%d")  # Get the current date as a string
    filename = f'todolist_{date_str}.csv'  # Create a filename with the current date
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
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        tasks = [row for row in reader]
    stdscr.addstr(tabulate(tasks, headers='keys', tablefmt='rounded_outline'))  # Displaying using tabulate
    stdscr.refresh()
    stdscr.getch()

def view(stdscr):
    stdscr.clear()
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f'todolist_{date_str}.csv'
    if not os.path.exists(filename):
        stdscr.addstr(0,0,f"You haven't planned for today yet")
        stdscr.refresh()
        stdscr.getch()
        main(stdscr)
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        tasks = [row for row in reader]
    stdscr.addstr(tabulate(tasks, headers='keys', tablefmt='rounded_outline'))  # Displaying using tabulate
    stdscr.refresh()
    stdscr.getch()

def delete(stdscr):
    stdscr.clear()
    task_to_remove = get_input(stdscr, 'Task to Remove: ')
    new_tasks = []
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f'todolist_{date_str}.csv'

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Task'] != task_to_remove:
                new_tasks.append(row)

    for idx, task in enumerate(new_tasks, start=1):
        task['Number'] = idx

    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Number', 'Task', 'Time', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_tasks)

def edit(stdscr):
    stdscr.clear()
    task_to_edit = get_input(stdscr, 'Task to Edit: ')
    edit_to_what = get_input(stdscr, 'Change it to: ')
    new_tasks = []
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f'todolist_{date_str}.csv'

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Task'] == task_to_edit:
                row['Task'] = edit_to_what
            new_tasks.append(row)

    for idx, task in enumerate(new_tasks, start=1):
        task['Number'] = idx

    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Number', 'Task', 'Time', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_tasks)

def mark(stdscr):

    stdscr.clear()
    task_to_mark = get_input(stdscr, 'Task You Completed: ')
    new_tasks = []
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f'todolist_{date_str}.csv'

    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Task'] == task_to_mark:
                row['Status'] = 'Completed'
            new_tasks.append(row)

    for idx, task in enumerate(new_tasks, start=1):
        task['Number'] = idx

    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Number', 'Task', 'Time', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(new_tasks)

if __name__ == "__main__":
    curses.wrapper(main)
