from email.policy import default
from django.db.models import Model, CharField, IntegerField, ManyToManyField, ForeignKey, CASCADE
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUser(AbstractUser):
    pass

class Professor(Model):
    id = CharField(primary_key=True, max_length=3)
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

class Module(Model):
    code = CharField(max_length=3)
    title = CharField(max_length=150)
    semester = IntegerField(
        validators=[
        MaxValueValidator(2),
        MinValueValidator(1)
        ]
    )
    year = IntegerField(
        validators=[
        MaxValueValidator(2022),
        MinValueValidator(2000)
        ]
    )
    professor = ManyToManyField("Professor")

class Rating(Model):
    user = ForeignKey(CustomUser, on_delete=CASCADE)
    professor = ForeignKey(Professor, on_delete=CASCADE)
    module = ForeignKey(Module, on_delete=CASCADE)
    value = IntegerField(
        validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
        ]
    )