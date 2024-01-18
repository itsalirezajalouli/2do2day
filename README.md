# 2DO2DAY : A Todolist Terminal Application
#### Video Demo:  <https://www.youtube.com/watch?v=XY6MAneGdW4>
#### Description:

I just wanted to make something I myself really needed, with this program you can write a to do list,add tasks to it for multiple times, view them, edit them and also mark them as completed. I heavily used a library called "curses" that exists in python standard libraries for the interface of the program and took a lot of time to figure out how it works. I hope you like this program and use it to be productive.

#### Features :

Dynamic Menus: Navigate through menu options such as viewing, adding, editing, or deleting tasks.

Interactive Prompts: Easily add or modify tasks with prompts for task information.

Real-Time Updates: View and mark tasks with their respective status in real-time, and keep track of your progress throughout the day.

Daily Task Segregation: Manage your tasks in daily segmented CSV files automatically named with the date for better organization.

Tabulated Display: Enjoy clear and structured visualization of tasks using the tabulate library.

#### Dependencies:

curses: For building the interactive menu and prompts within the terminal.

tabulate: To display tasks in a well-structured table format.

csv: For reading from and writing to CSV files, which store task data.

datetime: To handle date and time, vital for segregating task lists by day.

os: To check for the existence of files based on the current date.
