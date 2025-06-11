from fastapi import APIRouter, HTTPException, Query
from models.schames import StackArguments, Result, OperationEnum
from handlers.stack_handler import stack
from handlers.history_handler import history
from models.schames import FlavorEnum
from fastapi.responses import JSONResponse

from operations import calculate

router = APIRouter(prefix="/calculator/stack", tags=["stack"])

@router.get("/size" ,response_model=Result)
def get_stack_size():
    return JSONResponse(status_code=200, content=stack.size())

@router.put("/arguments", response_model=Result)
def push_arguments(arguments: StackArguments):
    try:
        result = stack.push(arguments.arguments)
        return JSONResponse(status_code=200, content=result)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/operate", response_model=Result)
def operate(operation: OperationEnum = Query(...)):
    try:
        arguments = stack.pop_operation(operation)
        result = calculate(operation, arguments)
        history.log(FlavorEnum.stack, operation.value, arguments, result)
        return JSONResponse(status_code=200, content=result)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/arguments")
def remove_arguments(count: int = Query(...)):
    try:
        size_after_delete = stack.remove(count)
        return JSONResponse(status_code=200, content=size_after_delete)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
