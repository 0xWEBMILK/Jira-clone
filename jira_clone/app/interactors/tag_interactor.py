from ..schemas import TagSchema


class TagInteractor:
    def __init__(self, repository, hasher):
        self.repository = repository
        self.hasher = hasher

    def get_tag_by_token(self, token):
        return self.repository.get_tag_by_token(token)

    def get_all_tags(self):
        tags = self.repository.get_all_tags()

        return None if len(tags) == 0 else tags

    def create_tag(self, tag_schema: TagSchema):
        token = self.hasher.encode(tag_schema)

        if self.get_tag_by_token(token) is None:
            self.repository.create_tag(token)

        return token

    def remove_tag(self, tag_schema: TagSchema):
        token = self.hasher.encode(tag_schema)

        if self.get_tag_by_token(token):
            self.repository.remove_tag(token)

            return token

        return None

    def update_tag(self, old_tag_schema: TagSchema, new_tag_schema: TagSchema):
        old_token = self.hasher.encode(old_tag_schema)
        new_token = self.hasher.encode(new_tag_schema)

        if self.get_tag_by_token(old_token):
            self.repository.update_tag(old_token, new_token)

            return new_token

        return None