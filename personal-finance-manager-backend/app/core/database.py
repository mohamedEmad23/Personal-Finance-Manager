from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://root:123Main_Connection123@localhost/finance_manager_sp"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# autocommit=False: Disables automatic commit of transactions. This allows you to group multiple operations into a single transaction and commit them together.
# autoflush=False: Disables automatic flushing of changes to the database. This means that changes to objects will not be immediately written to the database until you explicitly call the session.flush() or session.commit() methods.
Base = declarative_base()
