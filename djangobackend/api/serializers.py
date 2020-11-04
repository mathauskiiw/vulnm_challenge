from rest_framework import serializers
from .models import Asset, Vulnerability, VulnStatus, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username')


class VulnerabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Vulnerability
        fields = ['id', 'title', 'severity',
                  'cvss', 'pub_date', 'affected_count']


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ['id', 'hostname', 'ip_address', 'risk', 'vuln_count']


class VulnStatusSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(required=True)
    vulnerability = VulnerabilitySerializer(required=True)
    solved = serializers.BooleanField()

    class Meta:
        model = VulnStatus
        fields = ['solved', 'asset', 'vulnerability']


class PartialVulnStatusSerializer(serializers.ModelSerializer):
    solved = serializers.BooleanField()
    vulnerability = VulnerabilitySerializer(required=True)

    class Meta:
        model = VulnStatus
        fields = ['solved', 'vulnerability']


class AssetDetailSerializer(serializers.ModelSerializer):
    vulnstatus_set = PartialVulnStatusSerializer(many=True)

    class Meta:
        model = Asset
        fields = ['hostname', 'ip_address',
                  'risk', 'vuln_count', 'vulnstatus_set']
