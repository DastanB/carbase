import os
import logging

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from main.models import *
from main.serializers import *
from main.permissions import MainPermission
from main.filters import ComplectationFilter, OfferFilter

from diploma.tasks import send_mail_to_manager

logger = logging.getLogger(__name__)


# User = get_user_model()
# User.objects.create_superuser(os.environ.get("ADMIN_NAME"), os.environ.get("ADMIN_MAIL"), os.environ.get("ADMIN_PASSWORD"))

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (MainPermission,)
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    
    filterset_fields = ['name',]
    search_fields = ['name',]
    ordering_fields = ['name',]


    @action(methods=['GET'], detail=True, permission_classes=(AllowAny,), filter_backends=[DjangoFilterBackend, OrderingFilter, SearchFilter], filterset_fields=['name'], search_fields = ['name',], ordering_fields = ['name',])
    def saloons(self, request, pk):
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        city = get_object_or_404(City, id=pk)
        saloons = AutoSaloon.objects.filter(city_id=city.id)

        queryset = self.filter_queryset(saloons)

        page = paginator.paginate_queryset(queryset, request)
        serializer = AutoSaloonSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['name',]
    search_fields = ['name',]
    ordering_fields = ['name',]

    @action(methods=['GET'], detail=True, permission_classes=(AllowAny,), filter_backends=[DjangoFilterBackend, OrderingFilter, SearchFilter], filterset_fields=['name', 'mark__name', 'manufactured_in__name'], search_fields = ['name', 'mark__name', 'manufactured_in__name'], ordering_fields = ['name', 'mark__name', 'manufactured_in__name'])
    def cars(self, request, pk):
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        country = get_object_or_404(Country, id=pk)
        carmodels = AutoModel.objects.filter(manufactured_in_id=country.id)

        queryset = self.filter_queryset(carmodels)
        
        page = paginator.paginate_queryset(queryset, request)
        serializer = AutoModelSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

class AutoSaloonViewSet(viewsets.ModelViewSet):
    queryset = AutoSaloon.objects.all()
    serializer_class = AutoSaloonSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['name', 'city__name']
    search_fields = ['name', 'city__name']
    ordering_fields = ['name', 'city__name']

    @action(methods=['GET'], detail=True, permission_classes=(AllowAny,), filter_backends=[DjangoFilterBackend, OrderingFilter, SearchFilter], filterset_fields=['name', 'auto_saloon__name'], search_fields = ['name', 'auto_saloon__name'], ordering_fields = ['name', 'auto_saloon__name'])
    def marks(self, request, pk):
        paginator = LimitOffsetPagination()
        paginator.page_size = 20 

        saloon = get_object_or_404(AutoSaloon, id=pk)
        marks = AutoMark.objects.filter(auto_saloon_id=saloon.id)

        queryset = self.filter_queryset(marks)

        page = paginator.paginate_queryset(queryset, request)
        serializer = AutoMarkSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = AutoSaloon.objects.all()
        saloon = get_object_or_404(queryset, pk=pk)
        saloon.views += 1
        saloon.save()
        serializer = AutoSaloonSerializer(saloon)
        return Response(serializer.data)

class AutoMarkViewSet(viewsets.ModelViewSet):
    queryset = AutoMark.objects.all()
    serializer_class = AutoMarkSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['name', ]
    search_fields = ['name', ]
    ordering_fields = ['name', ]


    @action(methods=['GET'], detail=True, permission_classes=(AllowAny,), filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter], filterset_fields = ['name', 'mark__name', 'manufactured_in__name'], search_fields=['name', 'mark__name', 'manufactured_in__name'], ordering_fields=['name', 'mark__name', 'manufactured_in__name'])
    def cars(self, request, pk):
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        mark = get_object_or_404(AutoMark, id=pk)
        carmodels = AutoModel.objects.filter(mark_id=mark.id)

        queryset = self.filter_queryset(carmodels)

        page = paginator.paginate_queryset(queryset, request)
        serializer = AutoModelSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

class AutoModelViewSet(viewsets.ModelViewSet):
    queryset = AutoModel.objects.all()
    serializer_class = AutoModelSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    
    filterset_fields = ['name', 'mark__name', 'manufactured_in__name']
    search_fields = ['name', 'mark__name', 'manufactured_in__name']
    ordering_fields = ['name', 'mark__name', 'manufactured_in__name']

    @action(methods=['GET'], detail=True, filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter], filterset_fields = ['name', 'color', 'drive_train', 'gearbox', 'year', 'auto_model__name'], search_fields = ['name',], ordering_fields = ['name', 'color', 'drive_train', 'gearbox', 'year',])
    def complectations(self, request, pk):
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        model = get_object_or_404(AutoModel, id=pk)
        comps = Complectation.objects.filter(auto_model_id=model.id)

        queryset = self.filter_queryset(comps)

        page = paginator.paginate_queryset(queryset, request)
        serializer = ComplectationSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['name', 'type_of']
    search_fields = ['name', 'type_of']
    ordering_fields = ['name', 'type_of']

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['description',]
    search_fields = ['description',]
    ordering_fields = ['description',]

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['description',]
    search_fields = ['description',]
    ordering_fields = ['description',]

class ComplectationViewSet(viewsets.ModelViewSet):
    queryset = Complectation.objects.all()
    serializer_class = ComplectationSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # filterset_fields = ['name', 'color', 'engine_size', 'power', 'torque', 'drive_train', 'gearbox', 'year',]
    search_fields = ['name',] 
    ordering_fields = ['name', 'color', 'drive_train', 'gearbox', 'year',]
    filterset_class = ComplectationFilter

    @action(methods=['GET'], detail=True, filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter], filterset_class=OfferFilter, search_fields=['price', 'complectation__name'], ordering_fields=['price', 'complectation__name'])
    def offers(self, request, pk):
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        complectation = get_object_or_404(Complectation, id=pk)
        offs = Offer.objects.filter(complectation_id=complectation.id)

        queryset = self.filter_queryset(offs)

        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    
    # filterset_fields = ['price', 'complectation__name']
    ordering_fields = ['price', 'complectation__name']
    search_fields = ['price', 'complectation__name']
    filterset_class = OfferFilter

    def retrieve(self, request, pk=None):
        queryset = Offer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)
        offer.views += 1
        offer.save()
        serializer = OfferSerializer(offer)
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=True, permission_classes=())
    def apps(self, request, pk):
        instance = self.get_object()
        request.data['offer'] = instance.id
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail_to_manager(instance.creator.email, serializer.data["id"])
            logger.info(f'Message is sent to {instance.creator.email}')
            return Response(serializer.data)
        return Response(serializer.errors)

class ClassCarViewSet(viewsets.ModelViewSet):
    queryset = ClassCar.objects.all()
    serializer_class = ClassCarSerializer
    permission_classes = (MainPermission, )
    authentication_classes = ()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    
    # filterset_fields = ['price', 'complectation__name']
    ordering_fields = ['name']
    search_fields = ['name']
    filterset_class = OfferFilter
    
    @action(methods=['POST'], detail=True, permission_classes=())
    def cars(self, request, pk):
        paginator = LimitOffsetPagination()
        paginator.page_size = 20

        class_of = get_object_or_404(ClassCar, id=pk)
        cars = AutoModel.objects.filter(class_of_id=class_of.id)

        queryset = self.filter_queryset(cars)

        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def test(request):
    send_mail_to_manager("dastan211298@gmail.com", "1")
    return Response("ok")