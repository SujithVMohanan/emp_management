import base64
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from apps.users.models import Users
from django.db.models import Q
from django.db import transaction


class UserService:
    def __init__(self):
        pass

    def already_exists(self, data):
        user = Users.objects.filter(Q(username=data.get("username")) | Q(email=data.get("email")))
        if not user:
            return False
        
        if user.filter(username=data.get("username")).exists():
            raise ValidationError("Username already exists.")
        if user.filter(email=data.get("email")).exists():
             raise ValidationError("Email already exists.")
         
    @transaction.atomic
    def register_user_by_from_data(self, data):
        
        user          = Users()
        user.username = data.get("username")
        user.email    = data.get("email")
        user.set_password(data.get("password"))
        user.save()

        image_string = data.get("profile_image")

        if image_string and image_string.startswith("data:image"):
            try:
                fmt, imgstr = image_string.split(";base64,")

                user.image = ContentFile(
                    base64.b64decode(imgstr),
                    name=f"{user.username}.{fmt.split('/')[-1]}"
                )
                user.save(update_fields=["image"])

            except Exception as e:
                print(f"Error processing profile image: {e}")
                raise Exception(f"Failed to process profile image.{e}")
            finally:
                del image_string
                del imgstr

        return user
    

    @transaction.atomic
    def change_password(self, user, new_password):
        if user.check_password(new_password):
            raise ValidationError("Not allowed to use the same password.")
        
        user.set_password(new_password)
        user.save(update_fields=["password"])
        return user
    

    
    @transaction.atomic
    def profile_update(self, user, data):
        
        user.username = data.get("username")
        user.email    = data.get("email")
        if data.get("password"):
            user.set_password(data.get("password"))
        user.save()

        image_string = data.get("profile_image")

        if image_string and image_string.startswith("data:image"):
            try:
                fmt, imgstr = image_string.split(";base64,")

                user.image = ContentFile(
                    base64.b64decode(imgstr),
                    name=f"{user.username}.{fmt.split('/')[-1]}"
                )
                user.save(update_fields=["image"])

            except Exception as e:
                print(f"Error processing profile image: {e}")
                raise Exception(f"Failed to process profile image.{e}")
            finally:
                del image_string
                del imgstr

        return user
    
