from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

contract_status = [
    ('unsigned', '0'),
    ('signed', '1')
]
roles_list = [
    ('Sales', 'sales'),
    ('Support', 'support')
]

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError("You must enter an email")
        user = self.model(
            email=self.normalize_email(email)
        )
        # email = self.normalize_email(email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True,
                              max_length=255,
                              blank=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    password = models.TextField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    role = models.CharField(max_length=25,
                            choices=roles_list,
                            null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()


    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Contract(models.Model):
    sales_contact = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=8,
                              choices=contract_status,
                              default='unsigned')
    amount = models.FloatField()
    payment_due = models.DateTimeField()


class Event(models.Model):
    #contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    # contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    support_contact = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    event_status = models.ForeignKey(Contract, on_delete=models.CASCADE)

    attendees = models.IntegerField()
    event_date = models.DateTimeField(null=True)
    notes = models.CharField(max_length=200)
