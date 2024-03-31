from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError(_('The Username field must be set'))
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_company = models.BooleanField(_('company status'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=50)
    education = models.CharField(max_length=50)
    header= models.CharField(max_length=50, null=True)
    bio = models.CharField(max_length=200)
    contact = models.IntegerField()
    age = models.IntegerField()
    GEN= (
    ('F','Female'),
    ('M','Male'),
    )
    resume =  models.FileField(upload_to ='uploads/')
    gender = models.CharField(max_length=1, choices=GEN)
    location = models.CharField(max_length=50,null=True)
    pic = models.ImageField(upload_to='uploads/', null=True, blank=True)
    def __str__(self):
        return self.name

class CompanyProfile(models.Model):
    user= models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    contact = models.IntegerField()
    location = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    pic = models.ImageField(upload_to='uploads/', null=True, blank=True)
    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
 
class Jobs(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    salary = models.IntegerField()
    TYPE=(
        ('PT','part-time'),
        ('FT','full-time'),
        ('IN','internship'),
        ('RM','remote'),
        ('FL','freelance'),
    )
    jobtype = models.CharField(max_length=2,choices=TYPE)   
    location = models.CharField(max_length=50)
    apply_by= models.DateField()
    req_skills= models.ManyToManyField(Skill, related_name='jobs') 
    def __str__(self):
        return self.title

class Application(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    applied_date = models.DateField(auto_now_add=True)
    
    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)

    def approve(self):
        self.status = self.APPROVED
        self.save()

    def reject(self):
        self.status = self.REJECTED
        self.save()
        
    def __str__(self):
        return f"{self.profile.user.username} applied for {self.job.title} "


class BlogPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
    
