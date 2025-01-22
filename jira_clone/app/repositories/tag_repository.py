from sqlalchemy.orm import Session
from ..models import TagModel

class TagRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_tag(self, token: str):
        new_tag = TagModel(token=token)
        self.session.add(new_tag)
        self.session.commit()

    def remove_tag(self, token: str):
        tag = self.get_tag_by_token(token)
        self.session.delete(tag)
        self.session.commit()

    def update_tag(self, old_token: str, new_token: str):
        tag = self.get_tag_by_token(old_token)
        tag.token = new_token
        self.session.commit()

    def get_tag_by_token(self, token: str):
        return self.session.query(TagModel).filter_by(token=token).first()

    def get_all_tags(self):
        return self.session.query(TagModel).all()