from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        print("User profile created")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()

        except:
            # create the userprofile if not exist
            UserProfile.objects.create(user=instance)
            print("User profile not found, newly created")
        print("User profile updated")

             
# @receiver(pre_save, sender=User)
# def pre_save_create_profile_reciever(sender, instance, **kwargs):
#     print(instance.username, 'this user being saved')
        
# post_save.connect(post_save_create_profile_reciever, sender=User)
