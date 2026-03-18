from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from datetime import datetime
from .models import Book

class BookService:
    async def get_all_books(self, session:AsyncSession):
        print(f"Session ID: {id(session)}")
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result.all()
    
    async def get_book(self, book_uid:str, session:AsyncSession):
        print(f"Session ID: {id(session)}")
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)

        return result.first()

    async def create_book(self, book_data:BookCreateModel, session:AsyncSession):
        book_data_dict = book_data.model_dump()
        
        # Remove published_date from dict to handle conversion separately
        published_date_str = book_data_dict.pop('published_date')

        new_book = Book(
            **book_data_dict
        )

        new_book.published_date = datetime.strptime(published_date_str, "%Y-%m-%d").date()
        session.add(new_book)

        await session.commit()

        return new_book

    async def update_book(self, book_uid:str, update_book:BookUpdateModel, session:AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        update_data_dict = update_book.model_dump()
        if book_to_update is not None:
            for key, value in update_data_dict.items():
                if key == "published_date" and value is not None:
                    setattr(book_to_update, key, datetime.strptime(value, "%Y-%m-%d").date())
                else:
                    setattr(book_to_update, key, value)

            await session.commit()
            return book_to_update
        else:     
            return None

    async def delete_book(self, book_uid:str, session:AsyncSession):
        
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None