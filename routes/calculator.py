from fastapi import APIRouter, HTTPException,Query
from models.schames import FlavorEnum,Result, CalculationRequest
from handlers.history_handler import history
from fastapi.responses import JSONResponse
from init_services import independent_logger, request_counter


from operations import calculate

router = APIRouter(prefix="/calculator", tags=["calculator"])

@router.get("/health")
def health():
    return JSONResponse(status_code=200, content="OK")

@router.post("/independent/calculate", response_model=Result)
def independent_calculate(payload: CalculationRequest):
    try:
        result = calculate(payload.operation, payload.arguments)

        independent_logger.info(
            f"Performing operation {payload.operation}. Result is {int(result)}",
            extra={"request_id": request_counter["count"]}
        )

        independent_logger.debug(
            f"Performing operation: {payload.operation}({payload.arguments}) = {int(result)}",
            extra={"request_id": request_counter["count"]}
        )

        history.log(FlavorEnum.independent, payload.operation, payload.arguments, result)
        return JSONResponse(status_code=200, content={"result" : result})

    except ValueError as e:
        independent_logger.error(
            f"Server encountered an error! message: {str(e)}",
            extra={"request_id": request_counter["count"]}
        )
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/history", response_model=Result)
def get_history(flavor: FlavorEnum = Query(None)):
    return JSONResponse(status_code=200, content={"result": history.get_history(flavor)})


