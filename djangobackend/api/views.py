from .models import Host, Vulnerability
from .serializers import HostSerializer, VulnerabilitySerializer
from rest_framework import viewsets

class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer


class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer