# Task tracker
https://roadmap.sh/projects/task-tracker

Основные команды:
- task add (Task) - добавить задачу в список
- task delete (Task ID) - удалить задачу по id
- task update (Task ID) (New task) - обновить описание задачи по id
- task mark (Task ID) (New status ['todo', 'in-progress', 'done']) - пометить задачу как "нужно сделать" / "в процессе" / "сделано"
- task list ['todo', 'in-progress', 'done'] - отобразить список задач по статусу
- task help - отображение подсказок к командам
- task exit - выход

v1.1
Изменения:
- Переработано отслеживание команд
- Добавлена обработка множества исключения

v1.0
Изменения:
- Переработана структура проекта (разбиение 1 класса на 3 в зависимости от выполняемых действий)

