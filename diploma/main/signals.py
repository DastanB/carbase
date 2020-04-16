from django.db.models.signals import post_delete
from django.dispatch import receiver

from main.models import Image, Offer
from utils import offer_delete_path, offer_image_delete_path


@receiver(post_delete, sender=Offer)
def order_deleted(sender, instance, created=True, **kwargs):
    offer_delete_path(instance)


@receiver(post_delete, sender=Image)
def order_picture_deleted(sender, instance, created=True, **kwargs):
    offer_image_delete_path(instance.file)


