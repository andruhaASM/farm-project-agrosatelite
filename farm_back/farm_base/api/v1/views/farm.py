from rest_framework import generics

from farm_base.api.v1.serializers import FarmListSerializer, \
    FarmCreateSerializer, FarmDetailSerializer
from farm_base.models import Farm
from rest_framework import filters, fields, serializers
from django.shortcuts import get_object_or_404
from django.http import Http404


class FarmListCreateView(generics.ListCreateAPIView):
    serializer_class = FarmListSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FarmListSerializer
        else:
            return FarmCreateSerializer

    def perform_create(self, serializer):
        farm = serializer.save()
        area = float(farm.geometry.area)
        centroid = farm.geometry.centroid
        serializer.save(area=area, centroid=centroid)
    
    def get_queryset(self):
        if not self.request.query_params:
            return Farm.objects.filter(is_active=True)
        query_dict = {k: v for k, v in self.request.query_params.items() if v}
        filter_keyword_arguments_dict = {}
        for key, value in query_dict.items():
            if key == "municipality":
                filter_keyword_arguments_dict["municipality__icontains"] = value
            if key == "state_short_form":
                filter_keyword_arguments_dict["state_short_form__icontains"] = value
            if key == "id":
                filter_keyword_arguments_dict["id__exact"] = value
            if key == "name":
                filter_keyword_arguments_dict["name__icontains"] = value
            if key == "owner_name":
                filter_keyword_arguments_dict["owner_id__name__icontains"] = value
            if key == "owner_document":
                filter_keyword_arguments_dict["owner_id__document__exact"] = value
        queryset = Farm.objects.filter(is_active=True, **filter_keyword_arguments_dict)
        return queryset


class FarmRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Farm.objects.filter(is_active=True)
    serializer_class = FarmDetailSerializer