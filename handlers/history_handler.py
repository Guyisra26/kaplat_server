from models.schames import FlavorEnum

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
            return [entry for entry in self.history if entry["flavor"] == FlavorEnum.stack] + \
                   [entry for entry in self.history if entry["flavor"] == FlavorEnum.independent]
        return [entry for entry in self.history if entry["flavor"] == flavor]

history = HistoryLogger()