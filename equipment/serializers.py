from models import *
from rest_framework import serializers

class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ('id', 'equipment_type')

class EquipmentManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentManufacturer
        fields = ('id', 'manufacturer_name')

class EquipmentInfoSerializer(serializers.ModelSerializer):
    equipment_type_s = EquipmentTypeSerializer
    equipment_manufacturer = EquipmentManufacturerSerializer

    class Meta:
        model = EquipmentInfo
        fields = ('id', 'equipment_type', 'part_identifier', 'manufacturer_name',
                  'serial_number', 'date_of_manufacture', 'is_active')