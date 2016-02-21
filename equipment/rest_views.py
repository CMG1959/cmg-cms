from rest_framework import viewsets
from serializers import EquipmentTypeSerializer, EquipmentType


class EquipmentTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows equipment types to be viewed or edited
    """
    queryset = EquipmentType.objects.all().order_by('equipment_type')
    serializer_class = EquipmentTypeSerializer

