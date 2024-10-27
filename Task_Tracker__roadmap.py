import time
import json
from datetime import datetime

class TaskLogic:
    def __init__(self, file_name = 'data_file.json'):
        self.file_name = file_name
        self.tasks = []
        self.status_list = ['todo', 'in-progress', 'done']
        
    def load_tasks(self):   
        try:
            with open(self.file_name, 'r') as openedFile:
                self.tasks = json.load(openedFile)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self):
        with open(self.file_name, 'w') as openedFile:
            json.dump(self.tasks, openedFile)

    def get_task_by_id(self, task_id):
        self.load_tasks()
        try: 
            for task in self.tasks:
                if task['id'] == int(task_id): return task
        except ValueError:
            return None
        return None

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

    def update_task(self, task_id, description):
        task = self.get_task_by_id(task_id)
        if task is not None:
            task['description'] = ' '.join(description)
            task['updated_at'] = time.time()
            self.save_tasks()
            return task
        return None

    def recalculate_task_index(self):
        index = 1
        for task in self.tasks:
            task['id'] = index
            index += 1

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task is not None:
            self.tasks.remove(task)
            self.recalculate_task_index()
            self.save_tasks()
            return task
        return None

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
        for command in commands:
            help_text += f'\ntask {commands[command][1]}'
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
            'add': [2, 'add (Task)', {}],
            'delete': [3, 'delete (Task ID)', {}],
            'update': [3, 'update (Task ID) (New task)', {}],
            'mark': [4, 'mark (Task ID) (New status [todo / in-progress / done])', {}], 
            'list': [2, 'list [todo / in-progress / done]', {'todo': 3, 'in-progress': 3, 'done': 3}], 
            'help': [2, 'help', {}],
            'exit': [2, 'exit', {}]
        }

    def run(self):
        self.view.show_message('---Task list---')
        while True:
            user_input = self.view.get_user_input('\n>')
            command_parts = user_input.split()
            if len(command_parts) >= 2:            
                if command_parts[0] == 'task':
                    command = command_parts[1] 
                    if command in self.commands:
                        command_info = self.commands[command]                                            
                        if len(command_parts) > command_info[0]:
                            if command == 'add':
                                task = self.logic.add_task(' '.join(command_parts[2:]))
                                self.view.add_task_successfully(task['id'])
                            elif command == 'update':
                                task = self.logic.update_task(command_parts[2], command_parts[3:])
                                if task: self.view.update_task_successfully(task['id'])
                                else: self.view.invalid_parameter_error()
                            elif command == 'list' and len(command_parts) == command_info[0]+1:
                                if command_parts[2] in self.commands['list'][2]: status = command_parts[2] 
                                else:
                                    self.view.invalid_parameter_error()
                                    continue
                                task = self.logic.filter_tasks_by_status(status)
                                self.view.list_tasks(task, status)
                            else: self.view.invalid_command_error()
                        elif len(command_parts) == command_info[0]:
                            if command == 'delete':
                                task = self.logic.delete_task(command_parts[2])
                                if task: self.view.delete_task_successfully(task['id'])
                                else: self.view.invalid_parameter_error()
                            elif command == 'mark':
                                task = self.logic.mark_task(command_parts[2], command_parts[3])
                                if task: self.view.mark_task_successfully(task['id'], task['status'])
                                else: self.view.invalid_parameter_error()
                            elif command == 'help':
                                self.view.display_help(self.commands)
                            elif command == 'list':
                                task = self.logic.filter_tasks_by_status(None)
                                self.view.list_tasks(task, None)
                            elif command == 'exit':
                                exit()
                            else: self.view.invalid_parameter_error()
                        else: self.view.invalid_command_error()
                    else: self.view.invalid_command_error()
                else: self.view.invalid_command_error()
            else: self.view.invalid_command_error()

if __name__ == "__main__":
    logic = TaskLogic()
    view = TaskView()
    controller = TaskController(logic, view)
    controller.run()
