from fastapi import APIRouter, Depends
from src.books.book_data import books
from src.books.schemas import BookUpdateModel, BookCreateModel, Book
from fastapi import status, HTTPException, Query, Body
from typing import List
from src.db.main import get_session
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession

book_router = APIRouter()
book_service = BookService()

@book_router.get('/books', response_model = list[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)) -> list:
    books = await book_service.get_all_books(session)
    return books

@book_router.post('/books', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> Book:
    new_book = await book_service.create_book(book_data, session)
    return new_book

@book_router.get('/book/{book_uid}', response_model=Book)
async def get_book_by_id(book_uid: str, session: AsyncSession = Depends(get_session)) -> Book:
    book = await book_service.get_book(book_uid, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@book_router.patch('/book/{book_uid}', response_model=Book)
async def update_book(book_uid: str, book_update_data : BookUpdateModel, session: AsyncSession = Depends(get_session)) -> Book:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return updated_book

# The delete service returns an empty dictionary if the book is successfully deleted, 
# and None if the book is not found. The route handler checks the return value 
# and raises a 404 error if the book is not found, or returns a success message 
# if the deletion was successful. the emty dict will be falsy in case of if deleted_book condition.
# The values which make falsy is any empty datastructure, 0, false
@book_router.delete('/book/{book_uid}')
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    deleted_book = await book_service.delete_book(book_uid, session)
    if deleted_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"message": "Book deleted successfully"}