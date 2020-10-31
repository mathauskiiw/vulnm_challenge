from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from api.manager import CustomUserManager


class User(AbstractUser):
    objects = CustomUserManager()

class Host(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    # IP address REGEX validator 
    # ^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$
    ip_address = models.CharField(max_length=15, blank=False, unique=True)  
    
class Vulnerability(models.Model):
    SEV_OPT= (
        (1, 'Baixo'),
        (2, 'Médio'),
        (3, 'Alto'),
        (4, 'Crítico')
    )

    title = models.CharField(max_length=255, blank=False)
    severity = models.CharField(choices=SEV_OPT)
    cvss = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=False)
    publication_date = models.DateField(blank=False)
    host = models.ManyToManyField(Host)
