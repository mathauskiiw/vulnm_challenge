from .models import Asset, Vulnerability, VulnStatus
from .serializers import AssetSerializer, VulnerabilitySerializer, VulnStatusSerializer
from rest_framework import viewsets

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer


class VulnStatusViewSet(viewsets.ModelViewSet):
    queryset = VulnStatus.objects.all()
    serializer_class = VulnStatusSerializer