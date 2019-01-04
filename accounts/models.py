from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager







class UserManager(BaseUserManager):
    def create_user(self, email, first_name='', last_name='', password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("users must have an email address")

        user_obj = self.model(
            email=self.normalize_email(email)
        )

        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin
        user_obj.first_name = first_name
        user_obj.last_name = last_name

        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, first_name='', last_name='', password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        return user

    def create_superuser(self, email, first_name='', last_name='', password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_admin=True
        )
        super_trainer = Trainer.objects.create(user=user)
        super_trainer.user.first_name = 'Corey'
        super_trainer.user.last_name = 'Mclaughlin'
        super_trainer.save()

        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    time_stamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email and password are included by default

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True




class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=4, default='None', blank=True, null=True)

    def get_full_name(self):
        return self.user.get_full_name()

    def get_short_name(self):
        return self.user.get_short_name()

    def __str__(self):
        return self.get_full_name()


    # for navbar -- making connections to request.user possible in base.html

    def get_all_clients(self):
        all_clients = Client.objects.filter(trainer=self)
        return all_clients

    def get_all_trainers(self):
        return Trainer.objects.filter(user__is_staff=False)

    # def month_dues(self):
    #     month_sessions = Session.month.filter(trainer=self)
    #     if month_sessions <= 80:
    #         dues = month_sessions * 20
    #     else:
    #         undertime = 80 * 20
    #         overtime = 15 * (month_sessions - 80)
    #         dues = undertime + overtime
    #     return dues







class Client(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    pin = models.CharField(max_length=4, default='None', blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def current_week_sessions(self):
        pass

    def current_month_sessions(self):
        pass





USER_TYPES = (
    ('trainer', 'Trainer'),
    ('staff', 'Staff'),
    ('admin', 'Admin'),
)

class PreSetAuthorizedUser(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=255)
    code = models.CharField(max_length=15)
    type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return self.first_name + ' ' + self.last_name





