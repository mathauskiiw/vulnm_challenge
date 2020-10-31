from rest_framework import serializers
from .models import Host, Vulnerability


class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host
        fields = ['name', 'ip_address']


class VulnerabilitySerializer(serializers.HyperlinkedModelSerializer):
    # hosts = serializers.HyperlinkedIdentityField(
    #     view_name='host-detail',
    #     lookup_field='host',
    #     many=True
    # )
    
    class Meta:
        model = Vulnerability
        fields = ['title', 'severity', 'cvss', 'pub_date', 'hosts']