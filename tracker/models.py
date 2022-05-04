from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


EXPENSE_TYPES = [
    ('Расход', 'Расход'),
    ('Доход', 'Доход')
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    income = models.IntegerField(verbose_name='Доходы', default=0)
    outcome = models.IntegerField(verbose_name='Расходы', default=0)

    def __str__(self):
        return self.user.username


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except:
        Profile.objects.create(user=instance)


class Tag(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Название', max_length=50)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь',
                             to=User, on_delete=models.CASCADE)
    type = models.CharField(
        verbose_name='Тип', choices=EXPENSE_TYPES, max_length=12)
    amount = models.PositiveIntegerField(verbose_name='Количество')
    tag = models.ForeignKey(Tag, verbose_name='Теги',
                            on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(verbose_name='Дата', default=now)
    description = models.CharField(
        verbose_name='Описание', max_length=200, blank=True)

    def __str__(self):
        return self.description
