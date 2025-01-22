from ..models import Base

def init(engine):
    Base.metadata.create_all(engine)

def get_session_stub():
    pass