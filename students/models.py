from django.db import models

class Group(models.Model):
    name = models.CharField("Название группы", max_length=100)
    curator = models.CharField("Куратор", max_length=100)

    def __str__(self):
        return self.name

class Club(models.Model):
    name = models.CharField("Название клуба", max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    age = models.IntegerField("Возраст")
    group = models.ForeignKey(Group, verbose_name="Группа", on_delete=models.CASCADE)
    clubs = models.ManyToManyField(Club, verbose_name="Клубы", blank=True)
    photo = models.ImageField("Фотография", upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"