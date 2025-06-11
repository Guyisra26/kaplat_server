from models.schames import OperationEnum
from math import factorial

def normalize_operation(operation: str) -> OperationEnum:
    try:
        return OperationEnum(operation.lower()).value
    except ValueError:
        raise ValueError(f"Error: unknown operation: {operation}")
def validate_args(operation: str, args: list) -> OperationEnum:
    operation = normalize_operation(operation)
    arity = 1 if operation in {OperationEnum.abs, OperationEnum.fact} else 2

    if len(args) < arity:
        raise ValueError(f"Error: Not enough arguments to perform the operation {operation}")
    if len(args) > arity:
        raise ValueError(f"Error: Too many arguments to perform the operation {operation}")
    return operation

def calculate(operation: str, args: list) -> int:
    operation = validate_args(operation, args)
    print(operation)
    x = args[0]
    y = args[1] if len(args) > 1 else None
    try:
        match operation:
            case OperationEnum.plus:
                return x + y
            case OperationEnum.minus:
                return x - y
            case OperationEnum.times:
                return x * y
            case OperationEnum.divide:
                if y == 0:
                    raise ZeroDivisionError("Error while performing operation Divide: division by 0")
                return x / y
            case OperationEnum.pow:
                return x ** y
            case OperationEnum.abs:
                return abs(x)
            case OperationEnum.fact:
                if x < 0:
                    raise ValueError("Error while performing operation Factorial: not supported for the negative number")
                return factorial(x)
            case _:
                raise ValueError(f"Error: unknown operation: {operation}")
    except Exception as e:
        raise ValueError(f"Error in operation {operation}: {str(e)}")




