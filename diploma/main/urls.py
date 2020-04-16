from django.urls import path, include
from main.views import CityViewSet, CountryViewSet, ImageViewSet, OptionViewSet, AutoMarkViewSet, AutoModelViewSet, AutoSaloonViewSet, ComplectationViewSet, OfferViewSet, DiscountViewSet, test
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('test/', test),
]

router = routers.DefaultRouter()
router.register('cities', CityViewSet, )
router.register('countries', CountryViewSet, )
router.register('images', ImageViewSet, )
router.register('options', OptionViewSet, )
router.register('marks', AutoMarkViewSet, )
router.register('models', AutoModelViewSet, )
router.register('saloons', AutoSaloonViewSet, )
router.register('complectations', ComplectationViewSet, )
router.register('offers', OfferViewSet, )
router.register('discounts', DiscountViewSet, )


urlpatterns += router.urls