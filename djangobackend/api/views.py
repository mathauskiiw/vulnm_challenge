from .models import Asset, Vulnerability
from .serializers import AssetSerializer, VulnerabilitySerializer
from rest_framework import viewsets

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class VulnerabilityViewSet(viewsets.ModelViewSet):
    queryset = Vulnerability.objects.all()
    serializer_class = VulnerabilitySerializer