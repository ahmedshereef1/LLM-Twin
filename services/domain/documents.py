from .base import NoSQLBaseDocument


class UserDocument(NoSQLBaseDocument):
    first_name: str
    last_name: str

    class Settings:
        name = "users"

    @property
    def user_name(self):
        return f"{self.first_name} {self.last_name}"
