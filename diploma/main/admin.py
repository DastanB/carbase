from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin

from main.models import Country, AutoMark, AutoModel, AutoSaloon, Option, Offer, Complectation, Image, City, Discount, Application, ClassCar

# Register your models here.
@admin.register(Country)
class CountryAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')

    advanced_filter_fields = ('name',)

@admin.register(ClassCar)
class ClassCarAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'type_of')
    search_fields = ('id', 'name', 'type_of')

    advanced_filter_fields = ('name', 'type_of')


@admin.register(City)
class CityAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    
    advanced_filter_fields = ('name',)

@admin.register(AutoSaloon)
class AutoSaloonAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('city__name', 'name')
    raw_id_fields = ('city', 'marks')
    readonly_fields = ('creator', 'views')

    advanced_filter_fields = ('name', ('city__name', 'Город'))

    def get_queryset(self, request):
        user = request.user
        qs = super(AutoSaloonAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(creator=user)
        if user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.views = 0
        obj.save()

@admin.register(AutoMark)
class AutoMarkAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('id', 'name', )

    advanced_filter_fields = ('name',)

    def get_queryset(self, request):
        user = request.user
        qs = super(AutoMarkAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(creator=user)
        if user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

@admin.register(AutoModel)
class AutoModelAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'manufactured_in', 'mark')
    search_fields = ('id', 'name', 'mark__name', 'manifactured_in__name', 'class_of__name')
    raw_id_fields = ('manufactured_in', 'mark', 'class_of')
    readonly_fields = ('creator',)
    advanced_filter_fields = ('name', ('mark__name', 'Марка'), ('manifactured_in__name', 'Произведено в'), 'class_of')


    def get_queryset(self, request):
        user = request.user
        qs = super(AutoModelAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(creator=user)
        if user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

@admin.register(Complectation)
class ComplectationAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'auto_model')
    search_fields = ('id', 'name', 'auto_model__name')
    raw_id_fields = ('auto_model',)
    readonly_fields = ('creator',)
    advanced_filter_fields = ('name', 'color', 'engine_size', 'power', 'torque', 'drive_train', 'gearbox', 'year',)


    def get_queryset(self, request):
        user = request.user
        qs = super(ComplectationAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(creator=user)
        if user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

@admin.register(Option)
class OptionAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'type_of', 'name')
    search_fields = ('id', 'name', 'type_of')
    readonly_fields = ('creator',)
    advanced_filter_fields = ('name', 'type_of', )


    def get_queryset(self, request):
        user = request.user
        qs = super(OptionAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(creator=user)
        if user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()


@admin.register(Offer)
class OfferAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'price', 'complectation')
    search_fields = ('id', 'price', 'complectation__name')
    raw_id_fields = ('complectation', 'images', 'options', 'auto_saloon')
    readonly_fields = ('creator', 'views')
    advanced_filter_fields = ('price', ('complectation__name', 'Комплектация'))


    def get_queryset(self, request):
        user = request.user
        qs = super(OfferAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(creator=user)
        if user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.views = 0
        obj.save()

@admin.register(Image)
class ImageAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'description', 'file')
    search_fields = ('id', 'description')
    readonly_fields = ('creator',)
    advanced_filter_fields = ('description',)

    def get_queryset(self, request):
        user = request.user
        qs = super(ImageAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(creator=user)
        if user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

@admin.register(Discount)
class DiscountAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'description', 'title')
    search_fields = ('id', 'description', 'title')
    readonly_fields = ('creator',)
    advanced_filter_fields = ('description', 'title')

    def get_queryset(self, request):
        user = request.user
        qs = super(DiscountAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(creator=user)
        if user.is_superuser:
            return qs
        return qs
    
    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()

@admin.register(Application)
class ApplicationAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'phone', 'offer')
    search_fields = ('id', 'name', 'surname', 'phone', 'offer')
    advanced_filter_fields = ('name', 'surname', 'phone', 'offer')

    def get_queryset(self, request):
        user = request.user
        qs = super(ApplicationAdmin, self).get_queryset(request)

        if user.is_staff != user.is_superuser:
            return qs.filter(offer__creator=user)
        if user.is_superuser:
            return qs
        return qs