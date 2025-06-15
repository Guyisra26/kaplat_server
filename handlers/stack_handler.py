from collections import deque
from models.schames import OperationEnum
from typing import List
from init_services import stack_logger, request_counter


class StackHandler:
    def __init__(self):
        self.stack = deque()

    def size(self):
        current_size = len(self.stack)
        return current_size

    def get_stack_repr(self):
        return list(reversed(self.stack))

    def push(self, value):
        size_before = self.size()
        self.stack.extend(value)
        size_after = self.size()

        stack_logger.info(
            f"Adding total of {len(value)} argument(s) to the stack | Stack size: {size_after}",
            extra={"request_id": request_counter["count"]}
        )

        stack_logger.debug(
            f"Adding arguments: {','.join(str(v) for v in value)} | Stack size before {size_before} | stack size after {size_after}",
            extra={"request_id": request_counter["count"]}
        )

        return size_after

    def pop_operation(self, operation) -> List[int]:
        stack_size = len(self.stack)
        arity = 1 if operation in [OperationEnum.abs, OperationEnum.fact] else 2
        print(operation,arity)
        if stack_size < 0:
            raise ValueError(f"Error: cannot implement operation {operation.lower()}. It requires {arity} arguments and the stack has only {stack_size} arguments")
        if stack_size < arity:
            raise ValueError(f"Error: cannot implement operation {operation.lower()}. It requires {arity} arguments and the stack has only {stack_size} arguments")
        return [self.stack.pop() for i in range(arity)]

    def remove(self, count):
        stack_size = self.size()
        if stack_size < count:
            error_msg = f"Error: cannot remove {count} from the stack. It has only {stack_size} arguments"
            stack_logger.error(
                f"Server encountered an error! message: {error_msg}",
                extra={"request_id": request_counter["count"]}
            )
            raise ValueError(error_msg)

        for _ in range(count):
            self.stack.pop()

        size_after = len(self.stack)

        stack_logger.info(
            f"Removing total {count} argument(s) from the stack | Stack size: {size_after}",
            extra={"request_id": request_counter["count"]}
        )

        return {"result": size_after}

stack = StackHandler()

