from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import func
from datetime import date, datetime
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID,
            nullable = False,
            primary_key = True,
            default = uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=func.now(), onupdate=func.now(), nullable=False))

    def __repr__(self):  # magic method to return a string representation of the object
        return f"<Book {self.title}>"