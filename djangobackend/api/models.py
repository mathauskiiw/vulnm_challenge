from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, validate_ipv4_address
from django.utils.translation import gettext_lazy as _
from api.manager import CustomUserManager


class User(AbstractUser):
    objects = CustomUserManager()

class Host(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    # Considering only IPV4 addresses according to input file 
    ip_address = models.CharField(validators=[validate_ipv4_address], max_length=20, blank=False, unique=True)  
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Host, self).save(*args, **kwargs)

class Vulnerability(models.Model):
    
    title = models.CharField(max_length=255, blank=False)
    severity = models.CharField(max_length=50, blank=False)
    cvss = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=False)
    pub_date = models.DateField(blank=False)
    hosts = models.ManyToManyField(Host)

    def save(self, *args, **kwargs):
        self.severity = self.severity.lower()
        return super(Vulnerability, self).save(*args, **kwargs)

