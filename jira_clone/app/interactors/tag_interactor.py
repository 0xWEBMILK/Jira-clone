from ..schemas import TagSchema


class TagInteractor:
    def __init__(self, repository, hasher):
        self.repository = repository
        self.hasher = hasher

    def get_all_tags(self) -> list[str]:
        tags = list(map(lambda x: x.token, self.repository.get_all_tags()))

        return tags

    def get_tag_by_token(self, tag_token: str):
        encoded = self.repository.get_tag_by_token(tag_token)

        if encoded is not None:
            tag = self.hasher.decode(encoded.token)

            return tag

    def create_tag(self, tag_schema: TagSchema):
        token = self.hasher.encode(tag_schema)

        self.repository.create_tag(token)

        return token

    def remove_tag(self, tag_schema: TagSchema):
        token = self.hasher.encode(tag_schema)

        self.repository.remove_tag(token)

        return token

    def update_tag(self, old_tag_schema: TagSchema, new_tag_schema: TagSchema):
        old_token = self.hasher.encode(old_tag_schema)
        new_token = self.hasher.encode(new_tag_schema)

        self.repository.update_tag(old_token, new_token)

        return new_token