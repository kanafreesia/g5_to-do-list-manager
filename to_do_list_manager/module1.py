from datetime import datetime

class Task:
    def __init__(self, task, deadline=None):
        self.task = task
        self.deadline = deadline
        self.completed = False

    def __str__(self):
        return f"{self.task} (Deadline: {self.deadline})"

class PrioritizeTask(Task):
    def __init__(self, task, deadline=None, priority="Medium"):
        super().__init__(task, deadline)
        if priority not in ["High", "Medium", "Low"]:
            raise ValueError("Priority must be 'High', 'Medium', or 'Low'.")
        self.priority = priority

    def __str__(self):
        return f"{self.task} (Deadline: {self.deadline}, Priority: {self.priority})"

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, new_task, deadline=None, priority="Medium"):
        task = PrioritizeTask(new_task, deadline, priority)
        self.tasks.append(task)

    def edit_task(self, task, new_task, deadline=None, priority=None):
        task.task = new_task
        task.deadline = deadline
        if priority:
            if priority not in ["High", "Medium", "Low"]:
                raise ValueError("Priority must be 'High', 'Medium', or 'Low'.")
            task.priority = priority

    def delete_task(self, task):
        self.tasks.remove(task)

    def mark_completed(self, task):
        task.completed = True

    def get_tasks(self, completed=False):
        sorted_tasks = [
            task for task in self.tasks if task.completed == completed
        ]
        sorted_tasks.sort(
            key=lambda t: datetime.strptime(t.deadline, "%Y-%m-%d") if t.deadline else datetime.max
        )
        return sorted_tasks

