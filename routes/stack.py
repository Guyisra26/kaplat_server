from fastapi import APIRouter, HTTPException, Query
from models.schames import StackArguments, Result, OperationEnum
from handlers.stack_handler import stack
from handlers.history_handler import history
from models.schames import FlavorEnum
from fastapi.responses import JSONResponse
from init_services import stack_logger, request_counter


from operations import calculate

router = APIRouter(prefix="/calculator/stack", tags=["stack"])

@router.get("/size" ,response_model=Result)
def get_stack_size():
    stack_size = stack.size()
    stack_logger.info(
        f"Stack size is {stack_size}",
        extra={"request_id": request_counter["count"]}
    )
    stack_logger.debug(
        f"Stack content (first == top): {stack.get_stack_repr()}",
        extra={"request_id": request_counter["count"]}
    )
    return JSONResponse(status_code=200, content= {"result" : stack_size })

@router.put("/arguments", response_model=Result)
def push_arguments(arguments: StackArguments):
    try:
        result = stack.push(arguments.arguments)
        return JSONResponse(status_code=200, content={ "result" : result })
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/operate", response_model=Result)
def operate(operation: str = Query(...)):
    try:
        arguments = stack.pop_operation(operation)
        result = calculate(operation, arguments)

        stack_logger.info(
            f"Performing operation {operation}. Result is {result} | stack size: {stack.size()}",
            extra={"request_id": request_counter["count"]}
        )

        stack_logger.debug(
            f"Performing operation: {operation}({','.join(str(arg) for arg in arguments)}) = {result}",
            extra={"request_id": request_counter["count"]}
        )

        history.log(FlavorEnum.stack, operation, arguments, result)
        return JSONResponse(status_code=200, content={"result": result})

    except ValueError as e:
        stack_logger.error(
            f"Server encountered an error! message: {str(e)}",
            extra={"request_id": request_counter["count"]}
        )
        raise HTTPException(status_code=409, detail=str(e))

@router.delete("/arguments")
def remove_arguments(count: int = Query(...)):
    try:
        size_after_delete = stack.remove(count)
        return JSONResponse(status_code=200, content=size_after_delete)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
