from models import *
from rest_framework import serializers

class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ('equipment_type',)

class EquipmentManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentManufacturer
        fields = ('manufacturer_name',)

class EquipmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentInfo
        fields = ('equipment_type', 'part_identifier', 'manufacturer_name',
                  'serial_number', 'date_of_manufacture', 'is_active')
    # equipment_types = serializers.StringRelatedField(many=False)
    # equipment_manufacturer = serializers.StringRelatedField(many=False)
    equipment_type = EquipmentTypeSerializer(many=False)
    manufacturer_name = EquipmentManufacturerSerializer(many=False)
