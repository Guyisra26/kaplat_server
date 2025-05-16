from pydantic import BaseModel
from typing import List,Union,Optional
from enum import Enum

class OperationEnum(str,Enum):
    plus = "Plus"
    minus = "Minus"
    times = "Times"
    divide = "Divide"
    pow = "Pow"
    abs = "Abs"
    fact = "Fact"

class CalculationRequest(BaseModel):
    arguments: List[int]
    operation: str

class StackArguments(BaseModel):
    arguments: List[int]

class FlavorEnum(str,Enum):
    stack = "STACK"
    independent = "INDEPENDENT"

class HistoryEntry(BaseModel):
    flavor: FlavorEnum
    operation: str
    arguments: List[int]
    result: int

class Result(BaseModel):
    result: Optional[Union[int,List[HistoryEntry]]]
    error: Optional[str]