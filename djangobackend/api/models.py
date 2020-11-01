from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, validate_ipv4_address
from django.utils.translation import gettext_lazy as _
from api.manager import CustomUserManager


class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    """
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }
    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)


class CICharField(CaseInsensitiveFieldMixin, models.CharField):
    pass


class User(AbstractUser):
    objects = CustomUserManager()

class Asset(models.Model):
    hostname = CICharField(max_length=50, blank=False, unique=True)
     
    # Considering only IPV4 addresses according to input file 
    ip_address = models.CharField(validators=[validate_ipv4_address], max_length=20, blank=False, unique=True)  
    
    def __str__(self):
        return self.hostname

    def save(self, *args, **kwargs):
        self.hostname = self.hostname.lower()
        return super(Asset, self).save(*args, **kwargs)


class Vulnerability(models.Model):

    title = CICharField(max_length=255, unique=True, blank=False)
    severity = models.CharField(max_length=50, blank=False)
    cvss = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], null=True)
    pub_date = models.DateField(default=None, null=True)
    hosts = models.ManyToManyField(Asset, through='VulnStatus')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.severity = self.severity.lower()
        return super(Vulnerability, self).save(*args, **kwargs)


class VulnStatus(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    vulnerability = models.ForeignKey(
        Vulnerability, on_delete=models.PROTECT)
    solved = models.BooleanField(default=False)

    class Meta:
        # restricts a vulnerability to exist only once per host, and vice-versa
        unique_together = ('asset', 'vulnerability')
