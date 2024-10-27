import time
import json
from datetime import datetime

class TaskLogic:
    def __init__(self, file_name = 'data_file.json'):
        self.file_name = file_name
        self.tasks = []
        self.status_list = ['todo', 'in-progress', 'done']
        
    """Загружаем задачи из файла"""
    def load_tasks(self):   
        try:
            with open(self.file_name, 'r') as openedFile:
                self.tasks = json.load(openedFile)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    """Сохраняем задачи в файл"""
    def save_tasks(self):
        try:
            with open(self.file_name, 'w') as openedFile:
                json.dump(self.tasks, openedFile)
        except Exception as ex:
            print(f'Произошла ошибка при сохранении: {ex}')

    """Найти задачу по ID"""
    def get_task_by_id(self, task_id):
        self.load_tasks()
        try: 
            for task in self.tasks:
                if task['id'] == int(task_id): return task
        except ValueError:
            return None
        return None

    """Добавить новую задачу"""
    def add_task(self, description):
        self.load_tasks()
        if self.tasks:
            next_id = max(task['id'] for task in self.tasks)+1
        else:
            next_id = 1
        new_task = {
            'id': next_id,
            'description': description,
            'status': self.status_list[0],
            'created_at': time.time(),
            'updated_at': None
        }
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    """Обновить описание задачи"""
    def update_task(self, task_id, description):
        task = self.get_task_by_id(task_id)
        if task is not None:
            task['description'] = ' '.join(description)
            task['updated_at'] = time.time()
            self.save_tasks()
            return task
        return None

    """Пересчитать индекс"""
    def recalculate_task_index(self):
        index = 1
        for task in self.tasks:
            task['id'] = index
            index += 1

    """Удалить задачу по ID"""
    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task is not None:
            self.tasks.remove(task)
            self.recalculate_task_index()
            self.save_tasks()
            return task
        return None

    """Изменить статус задачи"""
    def mark_task(self, task_id, new_status):
        task = self.get_task_by_id(task_id)
        if task is not None and new_status in self.status_list:
            if task['status'] == new_status:
                return None
            else:
                task['status'] = new_status
                task['updated_at'] = time.time()
                self.save_tasks()
                return task
        return None

    """Получить список задач, отфильтрованный по статусу"""
    def filter_tasks_by_status(self, status = None):
        self.load_tasks()
        if status is None:
            return self.tasks
        return [task for task in self.tasks if task['status'] == status]

class TaskView:
    def show_message(self, message):
        print(message)

    def get_user_input(self, prompt: str):
        return input(prompt)

    def display_help(self, commands):
        help_text = '---Help---'
        for command, info in commands.items():
            help_text += f'\ntask {info[1]}'
        self.show_message(help_text)

    def list_tasks(self, tasks, status = None):
        if not tasks:
            if status is None: self.show_message('Task list empty')
            else: self.show_message(f"Task list with status '{status}' is empty")
        else:
            for task in tasks:
                created_at = datetime.fromtimestamp(task['created_at']).strftime('%Y-%m-%d %H:%M:%S')
                updated_at = datetime.fromtimestamp(task['updated_at']).strftime('%Y-%m-%d %H:%M:%S') if task['updated_at'] else 'None'
                self.show_message(f'{task['id']}. {task['description']} | {task['status']} | created at {created_at} | updated at {updated_at}')

    def add_task_successfully(self, task_id):
        self.show_message(f'Task added successfully (ID: {task_id})')

    def update_task_successfully(self, task_id):
        self.show_message(f'Task updated successfully (ID: {task_id})')

    def delete_task_successfully(self, task_id):
        self.show_message(f'Task deleted successfully (ID: {task_id})')

    def mark_task_successfully(self, task_id, new_status):
        self.show_message(f'Task marked successfully (ID: {task_id}, Status: {new_status})')

    def invalid_parameter_error(self):
        self.show_message(f'Invalid parameter')

    def invalid_command_error(self):
        self.show_message('Invalid command')

class TaskController():
    def __init__(self, logic, view):
        self.logic: TaskLogic = logic
        self.view: TaskView = view 
        self.commands = {
            'add': [self.handle_add, 'add (Task)'],
            'delete': [self.handle_delete, 'delete (Task ID)'],
            'update': [self.handle_update, 'update (Task ID) (New task)'],
            'mark': [self.handle_mark, f'mark (Task ID) (New status {self.logic.status_list})'], 
            'list': [self.handle_list, f'list {self.logic.status_list}'], 
            'help': [self.handle_help, 'help'],
            'exit': [self.handle_exit, 'exit']
        }

    def handle_add(self, args):
        if len(args) >= 1:
            task = self.logic.add_task(' '.join(args))
            self.view.add_task_successfully(task['id'])
        else: raise ValueError('task description not specified')

    def handle_delete(self, args):
        if len(args) == 1:
            task = self.logic.delete_task(args[0])
            if task: self.view.delete_task_successfully(task['id'])
            else: raise ValueError(f"task with number '{args[0]}' not found")
        else: raise ValueError('invalid number of arguments, please specify only the task number to be deleted')

    def handle_update(self, args):
        if len(args) >= 2:
            task = self.logic.update_task(args[0], args[1:])
            if task: self.view.update_task_successfully(task['id'])
            else: raise ValueError(f"task with number '{args[0]}' cannot be updated")
        else: raise ValueError('invalid number of arguments, please specify the task number to be changed and a new task description')

    def handle_mark(self, args):
        if len(args) == 2:
            task = self.logic.mark_task(args[0], args[1])
            if task: self.view.mark_task_successfully(task['id'], task['status'])
            else: raise ValueError(f"task with number '{args[0]}' not found, status '{args[1]}' unavailable or status '{args[1]}' already applied")
        else: raise ValueError(f'invalid number of arguments, please provide task number and new status {self.logic.status_list}')

    def handle_list(self, args):
        if len(args) == 0:
            task = self.logic.filter_tasks_by_status(None)
            self.view.list_tasks(task, None)
        elif len(args) == 1:
            if args[0] in self.logic.status_list:
                try:
                    task = self.logic.filter_tasks_by_status(args[0])
                    self.view.list_tasks(task, args[0])
                except IndexError: raise ValueError(f'invalid argument, please specify the task status {self.logic.status_list}')
            else: raise ValueError(f"status '{args[0]}' does not exist ")
        else: raise ValueError('invalid number of arguments')

    def handle_help(self, args = None):
        self.view.display_help(self.commands)

    def handle_exit(self, args = None):
        exit()

    def run(self):
        self.view.show_message('---Task list---')
        while True:
            user_input = self.view.get_user_input('\n>')
            command_parts = user_input.split()
            if len(command_parts) >= 2 and command_parts[0] == 'task':
                command = command_parts[1]
                if command in self.commands:
                    args = command_parts[2:]
                    try:
                        self.commands[command][0](args)
                    except Exception as ex:
                        self.view.show_message(f'Error: {ex}')
                else: self.view.invalid_command_error()
            else: self.view.invalid_command_error()

if __name__ == "__main__":
    logic = TaskLogic()
    view = TaskView()
    controller = TaskController(logic, view)
    controller.run()