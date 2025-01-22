from ..schemas import CategorySchema


class CategoryInteractor:
    def __init__(self, repository, hasher):
        self.repository = repository
        self.hasher = hasher

    def get_category_by_token(self, token):
        return self.repository.get_category_by_token(token)

    def get_all_categories(self):
        categories = self.repository.get_all_categories()

        return None if len(categories) == 0 else categories

    def create_category(self, category_schema: CategorySchema):
        token = self.hasher.encode(category_schema)

        if self.get_category_by_token(token) is None:
            self.repository.create_category(token)

        return token

    def remove_category(self, category_schema: CategorySchema):
        token = self.hasher.encode(category_schema)

        if self.get_category_by_token(token):
            self.repository.remove_category(token)

            return token

        return None

    def update_category(self, old_category_schema: CategorySchema, new_category_schema: CategorySchema):
        old_token = self.hasher.encode(old_category_schema)
        new_token = self.hasher.encode(new_category_schema)

        if self.get_category_by_token(old_token):
            self.repository.update_category(old_token, new_token)

            return new_token

        return None