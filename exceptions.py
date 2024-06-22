
class MaxTasksException(Exception):
    def __init__(self, message: str = 'Maximum tasks for one person!'):
        self.message = message

    def __str__(self) -> str:
        return self.message