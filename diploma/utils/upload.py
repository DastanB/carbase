import os
import shutil

def offer_image_path(instance, filename):
    return f'images/{instance.creator}/{filename}'


def offer_image_delete_path(document):
    path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(path)


def offer_delete_path(offer):
    if offer.images:
        path = os.path.abspath(os.path.join(offer.images[0].path, '../..'))
        shutil.rmtree(path)