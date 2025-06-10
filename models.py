from tortoise import fields
from tortoise.models import Model


class User(Model):
    user_id = fields.CharField(max_length=10, pk=True, description="账号")
    password = fields.CharField(max_length=10, description="密码")
    name = fields.CharField(max_length=20, description="用户名")


class Course(Model):
    cno = fields.IntField(pk=True)
    name = fields.CharField(max_length=30, description="课程名")


class Scores(Model):
    user = fields.ForeignKeyField("models.User", related_name="scores")
    cno = fields.ForeignKeyField("models.Course", related_name="scores1")
    score = fields.IntField(default=None)
