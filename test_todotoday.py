import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open
from todotoday import create, view, delete, edit, mark

@pytest.fixture
def stdscr_mock():
    return MagicMock()

@pytest.fixture
def date_mock():
    with patch('todotoday.datetime') as mock:
        mock.now.return_value = datetime(2023, 4, 1)
        yield mock

@pytest.fixture
def file_mock():
    with patch('todotoday.open', new_callable=mock_open, create=True) as mock:
        yield mock

@pytest.fixture
def writer_mock():
    with patch('todotoday.csv.DictWriter') as mock:
        yield mock

@pytest.fixture
def input_mock():
    with patch('todotoday.get_input') as mock:
        mock.side_effect = ['Test Task', '12:00']
        yield mock

@pytest.fixture
def task_number_mock():
    with patch('todotoday.get_task_number', return_value=1) as mock:
        yield mock

def test_create(stdscr_mock, date_mock, file_mock, writer_mock, input_mock, task_number_mock):
    create(stdscr_mock)

def test_view(stdscr_mock, file_mock):
    file_mock().read.return_value = 'Number,Task,Time,Status\n1,Test Task,12:00,Not Started\n'
    view(stdscr_mock)

def test_edit(stdscr_mock, file_mock, input_mock):
    file_content = "Number,Task,Time,Status\n1,Test Task,12:00,Not Started\n"
    m = mock_open(read_data=file_content)
    file_mock.side_effect = [m.return_value, m.return_value, m.return_value]
    input_mock.side_effect = ['Test Task', 'Edited Task']
    stdscr_mock.getstr.side_effect = ['Test Task', 'Edited Task']
    edit(stdscr_mock)

def test_delete(stdscr_mock, file_mock, input_mock):
    file_content = [
        ['Number', 'Task', 'Time', 'Status'],
        ['1', 'Test Task', '12:00', 'Not Started'],
        ['2', 'Another Task', '13:00', 'Not Started']
    ]
    file_mock().write.side_effect = [iter(file_content), iter([])]
    input_mock.side_effect = ['Test Task']
    delete(stdscr_mock)

def test_mark(stdscr_mock, file_mock, input_mock):
    file_mock().read.return_value = 'Number,Task,Time,Status\n1,Test Task,12:00,Not Started\n'
    input_mock.side_effect = ['Test Task']
    mark(stdscr_mock)
