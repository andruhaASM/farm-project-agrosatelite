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
        print(filter_keyword_arguments_dict)
        queryset = Farm.objects.filter(is_active=True, **filter_keyword_arguments_dict)
        return queryset

    # def get_object(self):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     if 'id' in self.request.query_params:
    #         filter_kwargs = {'id__exact': self.request.query_params['id']}
    #     elif 'state_short_form' in self.request.query_params:
    #          filter_kwargs = {'state_short_form__icontains': self.request.query_params['state_short_form']}
    #     elif 'municipality' in self.request.query_params:
    #          filter_kwargs = {'municipality__icontains': self.request.query_params['municipality']}
    #     elif 'name' in self.request.query_params:
    #          filter_kwargs = {'name__icontains': self.request.query_params['name']}
    #     elif 'owner_name' in self.request.query_params:
    #          filter_kwargs = {'owner_id__name': self.request.query_params['owner_name']}
    #     elif 'owner_document' in self.request.query_params:
    #          filter_kwargs = {'owner_id__document__exact': self.request.query_params['owner_document']}
    #     else:
    #         raise Http404('Missing required parameters')
    #     obj = get_object_or_404(queryset, **filter_kwargs)
    #     self.check_object_permissions(self.request, obj)
    #     return obj
    # def get_queryset(self):
    #     query_params = ValidateQueryParams(data=self.request.query_params)
    #     query_params.is_valid(raise_exception=True)
    #     queryset = Farm.objects.filter(is_active=True)
    #     # query_dict = {k: v for k, v in self.request.query_params.items() if v}
    #     # filter_keyword_arguments_dict = {}
    #     # for key, value in query_dict.items():
    #     #     if key == "municipality":
    #     #         filter_keyword_arguments_dict["municipality__icontains"] = value
    #     #     if key == "state_short_form":
    #     #         filter_keyword_arguments_dict["state_short_form__icontains"] = value
    #     #     if key == "id":
    #     #         filter_keyword_arguments_dict["id__exact"] = value
    #     #     if key == "name":
    #     #         filter_keyword_arguments_dict["name__icontains"] = value
    #     #     if key == "owner_name":
    #     #         filter_keyword_arguments_dict["owner_id__document__icontains"] = value
    #     #     if key == "owner_document":
    #     #         filter_keyword_arguments_dict["owner_id__document__exact"] = value
    #     # queryset = Farm.objects.filter(is_active=True, **filter_keyword_arguments_dict)
    #     return queryset


class FarmRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView):
    queryset = Farm.objects.filter(is_active=True)
    serializer_class = FarmDetailSerializer

# class FarmRetrieveView(generics.RetrieveAPIView):
#     queryset = Farm.objects.all()
#     serializer_class = FarmListSerializer

#     def get_object(self):
#         queryset = self.filter_queryset(self.get_queryset())
#         if 'id' in self.request.query_params:
#             filter_kwargs = {'id__exact': self.request.query_params['id']}
#         elif 'state_short_form' in self.request.query_params:
#              filter_kwargs = {'state_short_form__icontains': self.request.query_params['state_short_form']}
#         elif 'municipality' in self.request.query_params:
#              filter_kwargs = {'municipality__icontains': self.request.query_params['municipality']}
#         elif 'name' in self.request.query_params:
#              filter_kwargs = {'name__icontains': self.request.query_params['name']}
#         elif 'owner_name' in self.request.query_params:
#              filter_kwargs = {'owner_id__name': self.request.query_params['owner_name']}
#         elif 'owner_document' in self.request.query_params:
#              filter_kwargs = {'owner_id__document__exact': self.request.query_params['owner_document']}
#         else:
#             raise Http404('Missing required parameters')
#         obj = get_object_or_404(queryset, **filter_kwargs)
#         self.check_object_permissions(self.request, obj)
#         return obj
