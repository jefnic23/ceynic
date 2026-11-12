from fastapi import HTTPException, status
from sqlmodel import select

from src.database import ASYNC_SESSION_DEPENDENCY
from src.models.content import Content
from src.schemas.about_content import AboutContent


class ContentService:
    def __init__(self, session: ASYNC_SESSION_DEPENDENCY):
        self._session = session

    async def get_about(self, storefront_id: int) -> AboutContent:
        statement = select(Content).where(Content.storefront_id == storefront_id)
        result = await self._session.exec(statement)
        content = result.one_or_none()
        if content is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="About content not found"
            )
        return AboutContent(about=content.about)

    async def update_about(
        self, storefront_id: int, about: AboutContent
    ) -> AboutContent:
        if "blob:" in about.about.lower():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Blob URLs cannot be saved; use a public image URL instead",
            )

        statement = (
            select(Content)
            .where(Content.storefront_id == storefront_id)
            .with_for_update()
        )
        result = await self._session.exec(statement)
        content = result.one_or_none()
        if content is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="About content not found"
            )

        content.about = about.about
        await self._session.commit()
        return about
