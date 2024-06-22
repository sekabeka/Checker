import asyncio

from typing import Coroutine, List, Dict
from dataclasses import dataclass, field
from exceptions import MaxTasksException

@dataclass
class UserTasks:
    user: int
    max_tasks : int = 10
    tasks: List[Dict[str, asyncio.Task]] = field(default_factory=list)

    def add_task(self, name: str, coro: Coroutine, *args, **kwargs) -> None:
        if len(self.tasks) > self.max_tasks:
            raise MaxTasksException

        result: asyncio.Task = asyncio.ensure_future(coro(*args, **kwargs))
        result.set_name(name)
        self.tasks.append(
            {
                'Name' : name,
                'Task' : result
            }
        )

    def cancel_task(self, name: str):
        for d in self.tasks:
            if name in d:
                task = d['Task']
                task.cancel()
                self.tasks.pop(self.tasks.index(d))