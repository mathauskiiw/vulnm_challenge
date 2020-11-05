from django.conf import settings
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
    # Overwrites default User model to require only username and password
    objects = CustomUserManager()


class Asset(models.Model):
    # Case Insensitive charfield
    hostname = CICharField(max_length=50, blank=False, unique=True)

    # Considering only IPV4 addresses according to input file
    ip_address = models.CharField(
        validators=[validate_ipv4_address], max_length=20, blank=False, unique=True)

    @property
    def risk(self):
        # Dynamic property, simple mean of related vulnerabilities' risk
        queryset = self.vulns.filter(vulnstatus__solved=False)
        total = 0

        for i in queryset:
            if i.cvss:
                total += i.cvss

        return total/len(queryset)

    @property
    def vuln_count(self):
        # Count this asset's unsolved vulnerabilities
        return self.vulns.filter(vulnstatus__solved=False).count()

    @staticmethod
    def total_count():
        # Count all assets
        return Asset.objects.all().count()

    @staticmethod
    def total_infected():
        # Count all assets with at least 1 unsolved vulnerability
        count = 0
        for item in Asset.objects.all():
            if item.vuln_count > 1:
                count += 1

        return count

    @staticmethod
    def risk_mean():
        # Return the mean of all assets risk mean
        risk_mean_sum = 0
        count = 0
        for item in Asset.objects.all():
            risk_mean_sum += item.risk
            count += 1

        return risk_mean_sum/count

    @staticmethod
    def top_risk(qty):
        # Get the asset object list sorted by risk
        assets = sorted(Asset.objects.all(),
                        key=lambda m: m.risk, reverse=True)
        # Extract the hostname field from the Asset instances
        asset_names = list(map(lambda x: x.hostname, assets))

        # Number of assets returned -> qty
        return asset_names[:qty]

    def __str__(self):
        return self.hostname

    def save(self, *args, **kwargs):
        # Normalizes the data before saving
        self.hostname = self.hostname.lower()
        return super(Asset, self).save(*args, **kwargs)


class Vulnerability(models.Model):

    title = CICharField(max_length=255, unique=True, blank=False)
    severity = models.CharField(max_length=50, blank=False)
    cvss = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], null=True)
    pub_date = models.DateField(default=None, null=True)
    hosts = models.ManyToManyField(
        Asset, through='VulnStatus', related_name='vulns')

    def __str__(self):
        return self.title

    @property
    def affected_count(self):
        # Number of hosts affected by this vulnerability
        return self.hosts.filter(vulnstatus__solved=False).count()

    def save(self, *args, **kwargs):
        # Normalizes the data before saving
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

    def save(self, *args, **kwargs):
        # add save logic
        return super(VulnStatus, self).save(*args, **kwargs)

    @staticmethod
    def vuln_count_severity(severity):
        # Counts how many vulnerabilities are unsolved by severity
        count = VulnStatus.objects.filter(
            solved=False, vulnerability__severity=severity).count()
        return count
