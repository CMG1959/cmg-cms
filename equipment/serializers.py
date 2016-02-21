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
    equipment_types = serializers.StringRelatedField()
    equipment_manufacturers = serializers.StringRelatedField()

    class Meta:
        model = EquipmentInfo
        fields = ('id', 'equipment_types', 'part_identifier', 'equipment_manufacturers',
                  'serial_number', 'date_of_manufacture', 'is_active')