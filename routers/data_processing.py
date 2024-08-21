from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import StreamingResponse

from models.db import get_db_session
from schemas.data_processing import (
    TransformationRequest,
    SummaryResponse,
    TransformResponse,
    FileUploadResponse,
)
from services.file_manager import FileManager
from services.data_correction import DataCorrection
from services.visualizer import Visualizer

router = APIRouter()
file_manager = FileManager()


@router.post(
    "/upload",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    response_model=FileUploadResponse,
)
async def upload_file(
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
):
    try:
        file_id = file_manager.save_file(session, file=file.file)
        return {"message": "File uploaded successfully", "file_id": file_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File Upload Failed {str(e)}")


@router.get(
    "/summary/{file_id}",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    response_model=SummaryResponse,
)
async def get_summary(file_id: str):
    try:
        df = file_manager.load_file(file_id)

        return {
            "summary": {
                col: {
                    "mean": df[col].mean(),
                    "median": df[col].median(),
                    "std": df[col].std(),
                    "dtype": str(df[col].dtype),
                }
                for col in df.columns
            }
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"File not found {str(e)}")


@router.post(
    "/transform/{file_id}",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    response_model=TransformResponse,
)
async def transform_data(
    file_id: str,
    transformations: TransformationRequest,
    session: Session = Depends(get_db_session),
):
    try:
        df = file_manager.load_file(file_id)
        transformer = DataCorrection(df)

        if transformations.normalize:
            transformer.normalize(transformations.normalize)
        if transformations.fill_missing:
            transformer.fill_missing(transformations.fill_missing)

        return {
            "message": "Transformations applied successfully",
            "file_id": file_manager.save_file(session, df=df, file_id=file_id),
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"File not found {str(e)}")


@router.get(
    "/visualize/{file_id}",
    response_class=StreamingResponse,
    status_code=status.HTTP_200_OK,
)
async def visualize_data(file_id: str, chart_type: str, columns: str):
    try:
        df = file_manager.load_file(file_id)
        visualizer = Visualizer(df)
        columns = columns.split(",")
        return visualizer.visualize(chart_type, columns)

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"File not found in the system {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Bad Request {str(e)}")
