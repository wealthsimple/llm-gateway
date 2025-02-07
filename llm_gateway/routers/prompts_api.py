import datetime
import logging
from typing import List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)

from pydantic import BaseModel, Field

from llm_gateway.db.models import Prompt
from llm_gateway.db.utils import get_session

router = APIRouter()


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Human-readable error message")
    status_code: int = Field(503, description="HTTP status code")


def handle_sqlalchemy_error(exc: SQLAlchemyError) -> JSONResponse:
    error = ErrorResponse(
        detail="Database operation failed. Please try again later.", status_code=503
    )
    return JSONResponse(status_code=503, content=error.dict())


class PromptBase(BaseModel):
    title: str
    content: str
    theme: str


class PromptCreate(PromptBase):
    pass


class PromptResponse(PromptBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
        orm_mode = True
        json_encoders = {datetime.datetime: lambda v: v.isoformat()}


@router.get("/", response_model=List[PromptResponse])
def list_prompts():
    try:
        with get_session() as session:
            logging.info("Fetching all prompts from database")
            result = session.execute(select(Prompt))
            prompts = result.scalars().all()
            logging.info(f"Found {len(prompts)} prompts")
            return [PromptResponse.from_orm(p) for p in prompts]
    except SQLAlchemyError as e:
        logging.error(f"Database error in list_prompts: {str(e)}")
        raise SQLAlchemyError("Failed to load prompts")


@router.post("/", response_model=PromptResponse)
def create_prompt(prompt: PromptCreate):
    try:
        with get_session() as session:
            logging.info(f"Creating new prompt with title: {prompt.title}")
            db_prompt = Prompt(**prompt.dict())
            session.add(db_prompt)
            session.commit()
            session.refresh(db_prompt)
            logging.info(f"Successfully created prompt with id: {db_prompt.id}")
            return PromptResponse.from_orm(db_prompt)
    except SQLAlchemyError as e:
        logging.error(f"Database error in create_prompt: {str(e)}")
        raise SQLAlchemyError("Failed to create prompt")


@router.put("/{prompt_id}", response_model=PromptResponse)
def update_prompt(prompt_id: int, prompt: PromptCreate):
    try:
        with get_session() as session:
            logging.info(f"Updating prompt with id: {prompt_id}")
            result = session.execute(select(Prompt).where(Prompt.id == prompt_id))
            db_prompt = result.scalar_one_or_none()
            if not db_prompt:
                logging.warning(f"Prompt with ID {prompt_id} not found")
                raise HTTPException(
                    status_code=404, detail=f"Prompt with ID {prompt_id} not found"
                )

            for field, value in prompt.dict().items():
                setattr(db_prompt, field, value)

            session.commit()
            session.refresh(db_prompt)
            logging.info(f"Successfully updated prompt with id: {prompt_id}")
            return PromptResponse.from_orm(db_prompt)
    except SQLAlchemyError as e:
        logging.error(f"Database error in update_prompt: {str(e)}")
        raise SQLAlchemyError("Failed to update prompt")


@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: int):
    try:
        with get_session() as session:
            logging.info(f"Deleting prompt with id: {prompt_id}")
            result = session.execute(select(Prompt).where(Prompt.id == prompt_id))
            db_prompt = result.scalar_one_or_none()
            if not db_prompt:
                logging.warning(f"Prompt with ID {prompt_id} not found")
                raise HTTPException(
                    status_code=404, detail=f"Prompt with ID {prompt_id} not found"
                )

            session.delete(db_prompt)
            session.commit()
            logging.info(f"Successfully deleted prompt with id: {prompt_id}")
            return {"message": "Prompt deleted successfully"}
    except SQLAlchemyError as e:
        logging.error(f"Database error in delete_prompt: {str(e)}")
        raise SQLAlchemyError("Failed to delete prompt")
