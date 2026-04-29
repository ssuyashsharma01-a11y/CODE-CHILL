from app.db.session import engine
from app.models.domain import Base

def init_db_matrix():
    Base.metadata.create_all(bind=engine)
