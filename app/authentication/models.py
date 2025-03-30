from tortoise import fields
from tortoise.models import Model

class UserDB(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50)
    password = fields.CharField(max_length=100)
    mail = fields.CharField(max_length=50)
    year_of_birth = fields.IntField(null=True)

    class Meta:
        table = "users"

class UserBO:
    def __init__(self, username: str, password: str, mail: str, year_of_birth: int):
        self.username = username
        self.password = password
        self.mail = mail
        self.year_of_birth = year_of_birth
