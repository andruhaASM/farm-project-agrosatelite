from django.contrib.gis.geos import GEOSGeometry
from osgeo import ogr
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from farm_base.api.v1.serializers.owner import OwnerDetailSerializer, OwnerListCreateSerializer
from farm_base.models import Farm, Owner


class FarmListSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(FarmListSerializer, self).__init__(*args, **kwargs)
        request = kwargs['context']['request']
        include_geometry = request.GET.get('include_geometry', "false")

        if include_geometry.lower() == "true":
            self.fields['geometry'] = GeometryField(read_only=True)

    class Meta:
        model = Farm
        fields = ['name', 'owner_id', 'centroid', 'area', 'municipality', 'state_short_form']
        read_only_fields = ['id', 'centroid', 'area']

class FarmCreateSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(required=True)
    def validate_geometry(self, data):
        if data.hasz:
            g = ogr.CreateGeometryFromWkt(data.wkt)
            g.Set3D(False)
            data = GEOSGeometry(g.ExportToWkt())
        return data
    
    def validate_owner_id(self, data):
        try:           
            owner = Owner.objects.get(id=data)
        except:
            message = "Owner does not exist!"
            raise serializers.ValidationError(message)
        return owner.id
    
    def validate_municipality(self, data):
        if len(data) >= 2 and isinstance(data, str) and not data.isdigit():
            return data
        else:
            message = "Invalid municipality."
            raise serializers.ValidationError(message)

    def validate_state_short_form(self, data):
        if len(data) == 2 and isinstance(data, str) and not data.isdigit():
            return data
        else:
            message = f"Invalid state. State must be a string of 2 letters. E.g. SP. And not {data}"
            raise serializers.ValidationError(message)

    def validate_name(self, data):
        if len(data) >=2 and isinstance(data, str) and not data.isdigit():
            return data
        else:
            message = f"Invalid Farm name. Farm name must be a string of 2 or more letters. E.g. My Farm. And not {data}"
            raise serializers.ValidationError(message)

    class Meta:
        model = Farm
        fields = ['id', 'name', 'geometry', 'centroid', 'area', 'owner_id', 'municipality', 'state_short_form']
        read_only_fields = ['id', 'centroid', 'area', 'owner_id']


class FarmDetailSerializer(serializers.ModelSerializer):
    owner = OwnerDetailSerializer(read_only=True)

    class Meta:
        model = Farm
        fields = '__all__'
        read_only_fields = ['id', 'centroid', 'area']
