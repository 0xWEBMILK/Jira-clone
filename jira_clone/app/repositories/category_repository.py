from sqlalchemy.orm import Session
from ..models import CategoryModel

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, token: str):
        new_category = CategoryModel(token=token)
        self.session.add(new_category)
        self.session.commit()

    def remove_category(self, token: str):
        category = self.get_category_by_token(token)
        self.session.delete(category)
        self.session.commit()

    def update_category(self, old_token: str, new_token: str):
        category = self.get_category_by_token(old_token)
        category.token = new_token
        self.session.commit()

    def get_category_by_token(self, token: str):
        return self.session.query(CategoryModel).filter_by(token=token).first()

    def get_all_categories(self):
        return self.session.query(CategoryModel).all()