from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from main.models import City, Country, AutoMark, AutoSaloon, AutoModel, Complectation, Offer, Option, Image, Discount, Application, ClassCar
from main.constants import *

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class AutoMarkSerializer(ModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = AutoMark
        fields = '__all__'

class AutoSaloonSerializer(ModelSerializer):
    city = CitySerializer()
    images = ImageSerializer(many=True)
    marks = AutoMarkSerializer(many=True)
    
    class Meta:
        model = AutoSaloon
        fields = '__all__'

class AutoModelSerializer(ModelSerializer):
    manufactured_in = CountrySerializer()
    mark = AutoMarkSerializer()
    image = ImageSerializer()

    class Meta:
        model = AutoModel
        fields = '__all__'

class OptionSerializer(ModelSerializer):
    type_of = serializers.ChoiceField(choices=OPTION_TYPES, source='get_type_of_display')
    class Meta:
        model = Option
        fields = '__all__'

class ComplectationSerializer(ModelSerializer):
    color = serializers.ChoiceField(choices=COLORS, source='get_color_display')
    drive_train = serializers.ChoiceField(choices=DRIVE_TRAINS, source='get_drive_train_display')
    gearbox = serializers.ChoiceField(choices=GEARBOX_TYPES, source='get_gearbox_display')
    
    
    auto_model = AutoModelSerializer()
    class Meta:
        model = Complectation
        fields = '__all__'
        
class DiscountSerializer(ModelSerializer):    
    class Meta:
        model = Discount
        fields = '__all__'

class OfferSerializer(ModelSerializer):
    complectation = ComplectationSerializer()
    images = ImageSerializer(many=True)
    options = OptionSerializer(many=True)

    class Meta:
        model = Offer
        fields = '__all__'

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class ClassCarSerializer(ModelSerializer):
    class Meta:
        model = ClassCar
        fields = '__all__'