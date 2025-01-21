from jira_clone.app.schemas.schemas import CategorySchema


class CategoryInteractor:
    def __init__(self, repository, hasher):
        self.repository = repository
        self.hasher = hasher

    def get_all_categories(self) -> list[str]:
        categories = list(map(lambda x: x.token, self.repository.get_all_categories()))

        return categories

    def get_category_by_token(self, category_token: str):
        encoded = self.repository.get_category_by_token(category_token)

        if encoded is not None:
            category = self.hasher.decode(encoded.token)

            return category

    def create_category(self, category_schema: CategorySchema):
        token = self.hasher.encode(category_schema)

        self.repository.create_category(token)

        return token

    def remove_category(self, category_schema: CategorySchema):
        token = self.hasher.encode(category_schema)

        self.repository.remove_category(token)

        return token

    def update_category(self, old_category_schema: CategorySchema, new_category_schema: CategorySchema):
        old_token = self.hasher.encode(old_category_schema)
        new_token = self.hasher.encode(new_category_schema)

        self.repository.update_category(old_token, new_token)

        return new_token