from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import F
from .models import MenuItem

@receiver(post_save, sender=MenuItem)
def adjust_order_on_save(sender, instance, created, **kwargs):
    """
    Adjust orders when a MenuItem is added or updated.
    """
    if MenuItem.objects.filter(order=instance.order).exclude(id=instance.id).exists():
        # Shift all subsequent items' orders u[p by 1
        MenuItem.objects.filter(order__gte=instance.order).exclude(id=instance.id).update(order=F('order') + 1)

@receiver(pre_delete, sender=MenuItem)
def adjust_order_on_delete(sender, instance, **kwargs):
    """
    Adjust orders when a MenuItem is deleted.
    """
    # Shift all subsequent items' orders down by 1
    MenuItem.objects.filter(order__gt=instance.order).update(order=F('order') - 1)
