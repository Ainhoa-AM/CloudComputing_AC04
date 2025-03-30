from tortoise import fields
from tortoise.models import Model

class FileDB(Model):
    id = fields.UUIDField(pk=True)
    filename = fields.CharField(max_length=200)
    user = fields.CharField(max_length=50)

    class Meta:
        table = "files"
