from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)  # 'income' or 'expense'
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String(255), nullable=True)

    user = relationship("User", back_populates="transactions")