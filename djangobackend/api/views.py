from django.shortcuts import get_object_or_404
from .models import Asset, Vulnerability, VulnStatus, User
from .serializers import AssetSerializer, VulnerabilitySerializer, VulnStatusSerializer, UserSerializer, AssetDetailSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import generics


class AssetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def retrieve(self, request, pk=None):
        queryset = Asset.objects.all()
        asset = get_object_or_404(queryset, pk=pk)
        return Response(AssetDetailSerializer(asset, many=False).data)

    def list(self, request):
        queryset = Asset.objects.all()
        vuln_pk = self.request.query_params.get('vuln', None)
        if vuln_pk:
            queryset = queryset.filter(vulns__pk=vuln_pk, vulnstatus__solved=False)
        return Response(AssetSerializer(queryset, many=True).data)
        

class VulnerabilityListView(generics.ListAPIView):
    serializer_class = VulnerabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    
    def get_queryset(self):
        queryset = Vulnerability.objects.all()
        severity = self.request.query_params.get('severity', None)
        asset = self.request.query_params.get('asset', None)
        if severity:
            queryset = queryset.filter(severity=severity)
        if asset:
            queryset = queryset.filter(hosts__pk=asset)

        return queryset

    
class VulnStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VulnStatus.objects.all()
    serializer_class = VulnStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class VulnStatusUpdateView(generics.UpdateAPIView):
    serializer_class = VulnStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VulnStatus.objects.all()
    
    def get_object(self):
        obj = get_object_or_404(
            self.get_queryset(), 
            asset__pk=self.kwargs['asset_pk'], 
            vulnerability__pk=self.kwargs['vuln_pk']
        )

        return obj

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'solved': not instance.solved }, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

        



