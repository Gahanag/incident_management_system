from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import random
from django.utils import timezone
from django.conf import settings


class Abstracttime(models.Model):
    created_at=models.DateTimeField("Created_Date", auto_now_add=True)
    updated_at=models.DateTimeField("Updated_Date", auto_now=True)

    class Meta:
        abstract=True


class UserManager(BaseUserManager):
    def create_user(self, email, Reporter_Name,phone_number,Address,City,Country, Pin_code,password=None, password2=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            Reporter_Name=Reporter_Name,
            phone_number=phone_number,
            Address=Address,
            Pin_code=Pin_code,
            City=City,
            Country=Country,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, Reporter_Name, password=None):
            phone_number = ''  
            Address = ''       
            City = ''          
            Country = ''       
            Pin_code = ''      

            user = self.create_user(
                email,
                Reporter_Name=Reporter_Name,
                phone_number=phone_number,
                Address=Address,
                City=City,
                Country=Country,
                Pin_code=Pin_code,
                password=password
            )
            user.is_admin = True
            user.save(using=self._db)
            return user


class User(AbstractBaseUser , Abstracttime):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    Reporter_Name=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    Address=models.CharField(max_length=100)
    Pin_code=models.CharField(max_length=15)
    City=models.CharField(max_length=40)
    Country=models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["Reporter_Name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


FIELD_CHOICES = [
        ('G', 'Government'),
        ('E', 'Enterprise'),
    ]

PRIORITY_CHOICES = [
    ('H', 'High'),
    ('M', 'Medium'),
    ('L', 'Low'),
]


STATUS_CHOICES = [
    ('O', 'Open'),
    ('I', 'In Progress'),
    ('C', 'Closed'),
]

class Incident(models.Model):
    TITILE_OF_INCIDENT=models.CharField(max_length=100)
    incident_id = models.CharField( max_length=12, unique=True, editable=False)
    description = models.TextField()
    Incident_related_field = models.CharField(
        max_length=1,
        choices=FIELD_CHOICES,
        default='E',  
    )
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='M',  
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='O',  
    )

    created_by = models.ForeignKey(
        # settings.AUTH_USER_MODEL,
        User,
        on_delete=models.CASCADE,
        related_name='incidents',
    )

    

    def generate_incident_id(self):
        year = timezone.now().year
        random_number = random.randint(10000, 99999)
        self.incident_id = f'RMG{random_number}{year}'
    
    def save(self, *args, **kwargs):
        if not self.incident_id:
            self.generate_incident_id()
        super().save(*args, **kwargs)

      
    def __str__(self):
        return self.incident_id
    