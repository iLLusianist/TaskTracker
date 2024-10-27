import json
import time
from datetime import datetime

class Task:
    def __init__(self):
        self.jsonFileName = 'data_file.json'
        self.commandWord = 'task'
        self.tasks = []
        self.statusList = ['todo', 'in-progress', 'done']

        #command: [min_length, help_text, {subcommand: min_length}]
        self.commands = {
            'add': [2, 'add (Task)', {}],
            'delete': [3, 'delete (Task ID)', {}],
            'update': [3, 'update (Task ID) (New task)', {}],
            'mark': [4, 'mark (Task ID) (New status [todo / in-progress / done])', {}], 
            'list': [2, 'list [todo / in-progress / done]', {'todo': 3, 'in-progress': 3, 'done': 3}], 
            'help': [2, 'help', {}],
            'exit': [2, 'exit', {}]
            }

    def main_menu(self):
        print('---Task list---')
        while True:
            inputCommand = input('\n>')
            command = inputCommand.split()
            commandLen = len(command)
            if commandLen >= 2:
                if command[0] == self.commandWord:
                    if command[1] in self.commands:
                        commandInfo = self.commands[command[1]]
                        if commandLen > commandInfo[0]:
                            if command[1] == 'add':
                                self.add_tasks(' '.join(command[2:]))
                            elif command[1] == 'update':
                                self.update_task(command[2], command[3:])
                            elif command[1] == 'list' and commandLen == commandInfo[0]+1:
                                if command[2] in self.commands['list'][2]:
                                        self.list_tasks(command[2])
                                else: self.invalid_parameter()
                            else: self.invalid_parameter()
                        elif commandLen == commandInfo[0]:
                            if command[1] == 'delete':
                                self.delete_task(command[2])
                            elif command[1] == 'mark':
                                self.mark_task(command[2], command[3])
                            elif command[1] == 'help':
                                self.help_task()
                            elif command[1] == 'list':
                                self.list_tasks(None)
                            elif command[1] == 'exit':
                                exit()
                        else: self.invalid_parameter()
                    else: self.invalid_command()
                else: self.invalid_command()
            else: self.invalid_command()

    def invalid_parameter(self):
        print('Invalid parameter')

    def invalid_command(self):
        print('Invalid command')

    def help_task(self):
        helpText = f'---Help---\n'
        for command in self.commands:
            helpText += f'{self.commandWord} {self.commands[command][1]}\n'
        print(helpText)

    def add_tasks(self, task):
        self.load_tasks()
        if self.tasks == []:
            maxId = 0
        else:
            maxId = max(task['id'] for task in self.tasks)
        
        formatedTask = {
            'id': maxId+1,
            'desc': task,
            'status': self.statusList[0],
            'createdAt': time.time(),
            'updatedAt': None,
        }
        self.tasks.append(formatedTask)
        self.save_tasks(self.tasks)
        print(f'Task added successfully (ID: {maxId+1})')

    def delete_task(self, taskID):
        self.load_tasks()
        taskDeleted = False
        try:
            for task in self.tasks:
                if task['id'] == int(taskID):
                    self.tasks.remove(task)
                    taskDeleted = True
                    print(f'Task deleted successfully (ID: {taskID})')
            if taskDeleted: 
                newTaskID = 1
                for task in self.tasks:
                    task['id'] = newTaskID
                    newTaskID += 1
                    self.save_tasks(self.tasks)
            else: print ('Invalid value')
        except ValueError: print ('Invalid value')

    def update_task(self, taskID, newTask):
        self.load_tasks()
        taskUpdated = False
        try:
            for task in self.tasks:
                if task['id'] == int(taskID):
                    
                    task['desc'] = ' '.join(newTask)
                    task['updatedAt'] = time.time()
                    print(f'Task updated successfully (ID: {task['id']})')
                    self.save_tasks(self.tasks)
                    taskUpdated = True
            if not taskUpdated: print ('Invalid value')
        except ValueError: print ('Invalid value')

    def mark_task(self, taskID, newStatus):
        self.load_tasks()
        taskMarked = False
        try:
            if newStatus in self.statusList:
                for task in self.tasks:
                    if task['id'] == int(taskID):
                        if task['status'] == newStatus:
                            print (f'Task already {newStatus} (ID: {task['id']})')
                            taskMarked = True
                        else:
                            task['status'] = newStatus
                            task['updatedAt'] = time.time()
                            self.save_tasks(self.tasks)
                            print(f'Task marked successfully (ID: {task['id']}, Status: {newStatus})')
                            taskMarked = True
                if not taskMarked: print ('Invalid value')
            else: print ('Invalid value')
        except ValueError: print ('Invalid value')

    def save_tasks(self, task):
        with open(self.jsonFileName, 'w') as openedFile:
            json.dump(task, openedFile)

    def load_tasks(self):   
        try:
            with open(self.jsonFileName, 'r') as openedFile:
                self.tasks = json.load(openedFile)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def list_tasks(self, status):
        self.load_tasks()
        if status == None:
            self.print_tasks(self.tasks, None)
        else:
            tempTasks = []
            for task in self.tasks:
                if task['status'] == status:
                    tempTasks.append(task)
            self.print_tasks(tempTasks, status)

    def print_tasks(self, tasks, status):
        if tasks == []: 
            if status == None: print (f"Task list empty")
            else: print (f"Task list with status '{status}' empty")
        else:
            for task in tasks:
                print (f'{task['id']}. {task['desc']} | \
{task['status']} | created at {datetime.fromtimestamp(task['createdAt']).strftime('%Y-%m-%d %H:%M:%S')} | \
updated at {datetime.fromtimestamp(task['updatedAt']).strftime('%Y-%m-%d %H:%M:%S') if task['updatedAt'] else 'None'} ')

if __name__ == '__main__':
    Task().main_menu()


"""
Возможности:
    + Добавление, обновление и удаление задач
    + Пометьте задачу как выполняемую или выполненную
    + Список всех задач
    + Список всех выполненных задач
    + Список всех задач, которые не выполнены
    + Список всех выполняемых задач

Ограничения:
    + Используйте позиционные аргументы в командной строке для принятия пользовательских вводов.
    + Используйте файл JSON для хранения задач в текущем каталоге.
    + Файл JSON должен быть создан, если он не существует.
    + Используйте собственный модуль файловой системы вашего языка программирования для взаимодействия с файлом JSON.
    + Не используйте какие-либо внешние библиотеки или фреймворки для создания этого проекта.
    + Убедитесь, что ошибки и крайние случаи обрабатываются корректно.

Пример команд:
    task-cli add "Buy groceries"
    # Output: Task added successfully (ID: 1)
    task-cli update 1 "Buy groceries and cook dinner"
    task-cli delete 1
    task-cli mark-in-progress 1
    task-cli mark-done 1
    task-cli list
    task-cli list done
    task-cli list todo
    task-cli list in-progress

Свойства задачи:
    id: Уникальный идентификатор для задачи
    description: Краткое описание задачи
    status: Состояние задачи (todo, in-progress, done)
    createdAt: Дата и время создания задачи
    updatedAt: Дата и время последнего обновления задачи
    Не забудьте добавить эти свойства в файл JSON при добавлении новой задачи и обновить их при обновлении задачи.

Приступая к работе:
    + Настройте свою среду разработки
    + Выберите удобный для вас язык программирования (например, Python, JavaScript и т. д.).
    + Убедитесь, что у вас установлен редактор кода или интегрированная среда разработки (например, VSCode, PyCharm).
    + Инициализация проекта
    + Создайте новый каталог проекта для вашего интерфейса командной строки Task Tracker.
    Инициализируйте систему контроля версий (например, Git) для управления вашим проектом.

Функции реализации:
    + Начните с создания базовой структуры CLI для обработки пользовательских данных.
    + Реализуйте каждую функцию по очереди, тщательно тестируя каждую перед переходом к следующей. Например, сначала реализуйте функцию добавления задач, затем их перечисление, затем обновление, помечание как выполняемые и т. д.
    Тестирование и отладка
    + Протестируйте каждую функцию по отдельности, чтобы убедиться, что они работают должным образом. Посмотрите на файл JSON, чтобы убедиться, что задачи сохраняются правильно.
    + Устраняйте любые проблемы, возникающие в процессе разработки.
    + Завершение проекта
    + Убедитесь, что все функции реализованы и протестированы.
    Очистите свой код и добавьте комментарии там, где это необходимо.
    Напишите хороший файл readme о том, как использовать вашу CLI для отслеживания задач.
"""





'''
    def main_menu(self):
        print('---Task list---')
        while True:
            inputCommand = input('\n>')
            command = inputCommand.split()
            commandLen = len(command)
            if commandLen >= 2:
                if command[0] == self.commandWord:
                    if command[1] in self.commands:

                        if command[1] == 'add':
                            if commandLen >= self.commands['add'][0]:
                                self.add_tasks(' '.join(command[2:]))
                            else: print('Invalid parameter')

                        if command[1] == 'delete':
                            if commandLen >= self.commands['delete'][0]:
                                self.delete_task(command[2])
                            else: print('Invalid parameter')

                        if command[1] == 'list':
                            if commandLen == 3:
                                if command[2] in self.commands['list'][2]:
                                    self.list_tasks(command[2])
                                else: print('Invalid parameter')
                            elif commandLen ==2: self.list_tasks(None)
                            else: print('Invalid parameter')

                        if command[1] == 'update':
                            if commandLen >= self.commands['update'][0]:
                                self.update_task(command[2], command[3:])
                            else: print('Invalid parameter')

                        if command[1] == 'mark':
                            if commandLen == self.commands['mark'][0]:
                                self.mark_task(command[2], command[3])
                            else: print('Invalid parameter')

                        if command[1] == 'help':
                            if commandLen == self.commands['help'][0]:
                                self.help_task()
                            else: print('Invalid parameter')

                    else: print('Invalid command')
                else: print('Invalid command')
            else: print('Invalid command')
'''