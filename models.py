from sqlalchemy import Table, Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import metadata

expenses = Table(
    "expenses",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("category", String, nullable=True),
    Column("created_at", DateTime, server_default=func.now())
)
