from models.schames import FlavorEnum
from init_services import stack_logger, request_counter,independent_logger

class HistoryLogger:
    def __init__(self):
        self.history = []

    def log(self, flavor: FlavorEnum, operation: str, arguments: list, result: int):
        entry = {
            "flavor": flavor,
            "operation": operation,
            "arguments": arguments,
            "result": result
        }
        self.history.append(entry)

    def get_history(self,flavor: FlavorEnum = None):
        if flavor is None:
            from init_services import stack_logger
            stack_entries = [entry for entry in self.history if entry["flavor"] == FlavorEnum.stack]
            stack_logger.info(
                f"History: So far total {len(stack_entries)} stack actions",
                extra={"request_id": request_counter["count"]}
            )
            print(stack_entries)
            independent_entries = [entry for entry in self.history if entry["flavor"] == FlavorEnum.independent]
            independent_logger.info(
                f"History: So far total {len(independent_entries)} independent actions",
                extra={"request_id": request_counter["count"]}
            )
            return stack_entries + independent_entries

        if flavor == FlavorEnum.stack:
            from init_services import stack_logger
            stack_entries = [entry for entry in self.history if entry["flavor"] == FlavorEnum.stack]
            stack_logger.info(
                f"History: So far total {len(stack_entries)} stack actions",
                extra={"request_id": request_counter["count"]}
            )
            return stack_entries

        if flavor == FlavorEnum.independent:
            independent_entries = [entry for entry in self.history if entry["flavor"] == FlavorEnum.independent]
            independent_logger.info(
                f"History: So far total {len(independent_entries)} independent actions",
                extra={"request_id": request_counter["count"]}
            )
            return independent_entries

history = HistoryLogger()