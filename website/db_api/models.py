from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class TimedBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)


class User(TimedBaseModel):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    all_sop = (
        ('СТПВ', 'Ставрополь'),
        ('Омск', 'Омск'),
        ('ВЛГ', 'Волгоград'),
        ('СМР', 'Самара'),
    )

    user_id = models.BigIntegerField(verbose_name="ID Пользователя Телеграм", unique=True, primary_key=True)
    first_name = models.CharField(verbose_name="Имя пользователя", max_length=100)
    last_name = models.CharField(verbose_name="Фамилия пользователя", max_length=100)
    access = models.CharField(verbose_name="Доступ", max_length=100)
    role = models.CharField(verbose_name="Роль в секторе", max_length=100)
    status = models.CharField(verbose_name="Статус", max_length=100)
    photo = models.ImageField(upload_to='photo/', blank=True)
    sop = models.CharField(verbose_name="СОП", max_length=100, choices=all_sop, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name[:1]}."


class Quarter(TimedBaseModel):
    class Meta:
        verbose_name = "Квартал"
        verbose_name_plural = "Кварталы"

    quarter = models.IntegerField(verbose_name="Квартал", validators=[MinValueValidator(1), MaxValueValidator(4)])
    year = models.IntegerField(verbose_name="Год", validators= [MinValueValidator(1)])

    def __str__(self):
        return f"{self.quarter}Q"


class Bonus(TimedBaseModel):
    class Meta:
        verbose_name = "Бонус"
        verbose_name_plural = "Бонусы"

    id = models.AutoField(primary_key=True)
    initiator = models.ForeignKey(User, verbose_name="Инициатор", on_delete=models.SET(0), related_name='bonus_initiator')
    employee = models.ForeignKey(User, verbose_name="Сотрудник", on_delete=models.SET(0), related_name='bonus_employee')
    quarter = models.ForeignKey(Quarter, verbose_name="Квартал", on_delete=models.SET(0), related_name='bonus_quarter')
    activity = models.CharField(verbose_name="Активность", max_length=200, null=True)
    comment = models.CharField(verbose_name="Комментарий", max_length=200, null=True)
    criterion = models.CharField(verbose_name="Критерий", max_length=200, null=True)

    def __str__(self):
        return f"№{self.id} - {self.employee} {self.activity}"


class Mistake(TimedBaseModel):
    class Meta:
        verbose_name = "Ошибка"
        verbose_name_plural = "Ошибки"

    id = models.AutoField(primary_key=True)
    initiator = models.ForeignKey(User, verbose_name="Инициатор", on_delete=models.SET(0), related_name='mistake_initiator')
    employee = models.ForeignKey(User, verbose_name="Сотрудник", on_delete=models.SET(0), related_name='mistake_employee')
    quarter = models.ForeignKey(Quarter, verbose_name="Квартал", on_delete=models.SET(0), related_name='mistake_quarter')
    activity = models.CharField(verbose_name="Активность", max_length=200, null=True)
    comment = models.CharField(verbose_name="Комментарий", max_length=200, null=True)
    criterion = models.CharField(verbose_name="Критерий", max_length=200, null=True)

    def __str__(self):
        return f"№{self.id} - {self.employee} {self.activity}"


class Like(TimedBaseModel):
    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    id = models.AutoField(primary_key=True)
    initiator = models.ForeignKey(User, verbose_name="Инициатор", on_delete=models.SET(0), related_name='like_initiator')
    employee = models.ForeignKey(User, verbose_name="Сотрудник", on_delete=models.SET(0), related_name='like_employee')
    quarter = models.ForeignKey(Quarter, verbose_name="Квартал", on_delete=models.SET(0), related_name='like_quarter')

    def __str__(self):
        return f"{self.initiator} поставил лайк {self.employee}"


