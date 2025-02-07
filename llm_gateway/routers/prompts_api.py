from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from llm_gateway.db.models import Prompt
from llm_gateway.db.utils import get_session
from pydantic import BaseModel

router = APIRouter()


class PromptBase(BaseModel):
    title: str
    content: str
    theme: str


class PromptCreate(PromptBase):
    pass


class PromptResponse(PromptBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[PromptResponse])
async def list_prompts():
    async with get_session() as session:
        result = await session.execute(select(Prompt))
        prompts = result.scalars().all()
        return prompts


@router.post("/", response_model=PromptResponse)
async def create_prompt(prompt: PromptCreate):
    async with get_session() as session:
        db_prompt = Prompt(**prompt.dict())
        session.add(db_prompt)
        await session.commit()
        await session.refresh(db_prompt)
        return db_prompt


@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(prompt_id: int, prompt: PromptCreate):
    async with get_session() as session:
        result = await session.execute(
            select(Prompt).where(Prompt.id == prompt_id)
        )
        db_prompt = result.scalar_one_or_none()
        if not db_prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")

        for field, value in prompt.dict().items():
            setattr(db_prompt, field, value)

        await session.commit()
        await session.refresh(db_prompt)
        return db_prompt


@router.delete("/{prompt_id}")
async def delete_prompt(prompt_id: int):
    async with get_session() as session:
        result = await session.execute(
            select(Prompt).where(Prompt.id == prompt_id)
        )
        db_prompt = result.scalar_one_or_none()
        if not db_prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")

        await session.delete(db_prompt)
        await session.commit()
        return {"message": "Prompt deleted successfully"}
