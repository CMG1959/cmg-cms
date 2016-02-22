from models import *
from rest_framework import serializers

class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ('id', 'equipment_type',)

class EquipmentManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentManufacturer
        fields = ('id', 'manufacturer_name',)

class EquipmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentInfo
        fields = ('id', 'equipment_type', 'part_identifier', 'manufacturer_name',
                  'serial_number', 'date_of_manufacture', 'is_active')

    equipment_type = EquipmentTypeSerializer(many=False)
    manufacturer_name = EquipmentManufacturerSerializer(many=False)

    def create(self, validated_data):
        equipment_type_val = validated_data.pop('equipment_type')
        manufacturer_name_val = validated_data.pop('manufacturer_name')

        equipment_type = EquipmentType.objects.get_or_create(equipment_type=equipment_type_val)
        manufacturer_name = EquipmentManufacturer.objects.get_or_create(manufacturer_name=manufacturer_name_val)

        equipment_info = EquipmentInfo.objects.create(equipment_type=equipment_type,
                                                      manufacturer_name=manufacturer_name, **validated_data)
        return equipment_info

