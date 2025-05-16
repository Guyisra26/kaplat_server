from collections import deque
from models.schames import OperationEnum
from typing import List

class StackHandler:
    def __init__(self):
        self.stack = deque()

    def size(self):
        return len(self.stack)

    def push(self, value):
        self.stack.extend(reversed(value))
        return self.size()

    def pop_operation(self, operation) -> List[int]:
        if self.size() < 0:
            raise ValueError("Not enough elements in the stack to perform operation")
        arity = 1 if operation in [OperationEnum.abs, OperationEnum.fact] else 2
        if self.size() < arity:
            raise ValueError("Not enough elements in the stack to perform operation")
        return [self.stack.pop() for i in range(arity)]

    def remove(self, count):
        if self.size() < count:
            raise ValueError("Not enough elements in the stack to remove")
        for i in range(count):
            self.stack.pop()
        return self.size()

stack = StackHandler()

