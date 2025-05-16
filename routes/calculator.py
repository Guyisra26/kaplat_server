from fastapi import APIRouter, HTTPException,Query
from models.schames import FlavorEnum,Result, CalculationRequest
from handlers.history_handler import history
from fastapi.responses import JSONResponse

from operations import calculate

router = APIRouter(prefix="/calculator", tags=["calculator"])

@router.get("/health")
def health():
    return JSONResponse(status_code=200, content="OK")

@router.post("/independent/calculate", response_model=Result)
def independent_calculate(req: CalculationRequest):
    try:
        result = calculate(req.operation, req.arguments)
        history.log(FlavorEnum.independent, req.operation, req.arguments, result)
        return JSONResponse(status_code=200, content={"result": result})
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/stack/history", response_model=Result)
def get_history(flavor: FlavorEnum = Query(None)):
    result = history.get_history(flavor)
    return JSONResponse(status_code=200, content=result)

