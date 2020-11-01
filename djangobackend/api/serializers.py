from rest_framework import serializers
from .models import Asset, Vulnerability


class AssetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asset
        fields = ['hostname', 'ip_address']


class VulnerabilitySerializer(serializers.HyperlinkedModelSerializer):
    # hosts = serializers.HyperlinkedIdentityField(
    #     view_name='host-detail',
    #     lookup_field='host',
    #     many=True
    # )
    
    class Meta:
        model = Vulnerability
        fields = ['title', 'severity', 'cvss', 'pub_date', 'hosts']