from rest_framework import viewsets
from serializers import EquipmentTypeSerializer, EquipmentType,\
                        EquipmentManufacturerSerializer, EquipmentManufacturer,\
                        EquipmentInfoSerializer, EquipmentInfo


class EquipmentTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows equipment types to be viewed or edited
    """
    queryset = EquipmentType.objects.all().order_by('equipment_type')
    serializer_class = EquipmentTypeSerializer


class EquipmentManufacturerViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentManufacturerSerializer
    queryset = EquipmentManufacturer.objects.all().order_by('manufacturer_name')


class EquipmentInfoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentInfoSerializer
    queryset = EquipmentInfo.objects.all().order_by('part_identifier')
