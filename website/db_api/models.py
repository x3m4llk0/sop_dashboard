from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager

# Create your models here.
all_sop = (
    ('stvp', 'Ставрополь'),
    ('omsk', 'Омск'),
    ('vlg', 'Волгоград'),
    ('smr', 'Самара'),
)

all_role = (
    ('analyst', 'Аналитик'),
    ('expert', 'Эксперт'),
    ('ns', 'Начальник сектора')
)

class TimedBaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TgUser(models.Model):
    user_id = models.BigIntegerField(verbose_name="ID Пользователя Телеграм", unique=True, null=False, blank=True, primary_key=True)
    first_name = models.CharField(verbose_name="Имя", max_length=100, null=True, blank=True)
    last_name = models.CharField(verbose_name="Фамилия", max_length=100, null=True, blank=True)
    access = models.CharField(verbose_name="Доступ", max_length=100, null=True, blank=True)
    role = models.CharField(verbose_name="Роль в секторе", choices=all_role, max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='photo/', null=True, blank=True)
    sop = models.CharField(verbose_name="СОП", max_length=100, choices=all_sop, null=True, blank=True)

class SiteUser(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    id = models.AutoField(primary_key=True)
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    email = models.EmailField(_("email address"), blank=True)
    user_id = models.ForeignKey(TgUser, verbose_name="TG_ID", on_delete=models.CASCADE, blank=True, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser





class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    all_access = (
        ('user', 'Пользователь'),
        ('agreement', 'Согласующий')
    )

    user_id = models.BigIntegerField(verbose_name="ID Пользователя Телеграм", unique=True, null=False, blank=True, primary_key=True)
    access = models.CharField(verbose_name="Доступ", choices=all_access, max_length=100, null=True, blank=True)
    role = models.CharField(verbose_name="Роль в секторе", choices=all_role, max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='photo/', null=True, blank=True)
    sop = models.CharField(verbose_name="СОП", max_length=100, choices=all_sop, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}. {self.get_sop_display()}"


class Quarter(models.Model):
    class Meta:
        verbose_name = "Квартал"
        verbose_name_plural = "Кварталы"

    quarter = models.IntegerField(verbose_name="Квартал", validators=[MinValueValidator(1), MaxValueValidator(4)])
    year = models.IntegerField(verbose_name="Год", validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quarter}Q"


class Bonus(TimedBaseModel):
    class Meta:
        verbose_name = "Бонус"
        verbose_name_plural = "Бонусы"

    id = models.AutoField(primary_key=True)
    initiator = models.ForeignKey(TgUser, verbose_name="Инициатор", on_delete=models.CASCADE, related_name='bonus_initiator')
    employee = models.ForeignKey(TgUser, verbose_name="Сотрудник", on_delete=models.CASCADE, related_name='bonus_employee')
    quarter = models.ForeignKey(Quarter, verbose_name="Квартал", on_delete=models.CASCADE, related_name='bonus_quarter')
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
    initiator = models.ForeignKey(TgUser, verbose_name="Инициатор", on_delete=models.CASCADE, related_name='mistake_initiator')
    employee = models.ForeignKey(TgUser, verbose_name="Сотрудник", on_delete=models.CASCADE, related_name='mistake_employee')
    quarter = models.ForeignKey(Quarter, verbose_name="Квартал", on_delete=models.CASCADE, related_name='mistake_quarter')
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
    initiator = models.ForeignKey(TgUser, verbose_name="Инициатор", on_delete=models.CASCADE, related_name='like_initiator')
    employee = models.ForeignKey(TgUser, verbose_name="Сотрудник", on_delete=models.CASCADE, related_name='like_employee')
    quarter = models.ForeignKey(Quarter, verbose_name="Квартал", on_delete=models.CASCADE, related_name='like_quarter')

    def __str__(self):
        return f"{self.initiator} поставил лайк {self.employee}"


