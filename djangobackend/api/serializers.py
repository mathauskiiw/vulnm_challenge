from rest_framework import serializers
from .models import Asset, Vulnerability, VulnStatus


class VulnerabilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vulnerability
        fields = ['title', 'severity', 'cvss', 'pub_date', 'hosts']


class AssetSerializer(serializers.ModelSerializer):
    # vulns = VulnerabilitySerializer(many=True, queryset=Vulnerability.objects.all())
    class Meta:
        model = Asset
        fields = ['hostname', 'ip_address', 'risk', 'vuln_count']
    

class VulnStatusSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(required=True)
    vulnerability = VulnerabilitySerializer(required=True)
    solved = serializers.BooleanField()

    class Meta:
        model = VulnStatus
        fields = ['solved', 'asset', 'vulnerability']