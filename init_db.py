from database import engine, Base
from models import Users, Records, Conversations

Base.metadata.create_all(bind=engine)
