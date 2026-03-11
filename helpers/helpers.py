import base64
import uuid
from django.core.files.base import ContentFile


def base64_to_image(base64_string):

    if ';base64,' in base64_string:
        format, imgstr = base64_string.split(';base64,')
        ext = format.split('/')[-1]
    else:
        imgstr = base64_string
        ext = "png"

    file_name = f"{uuid.uuid4()}.{ext}"

    return ContentFile(base64.b64decode(imgstr), name=file_name)


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
    

