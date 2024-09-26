# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, UpdateOrder

@receiver(post_save, sender=Order)
def create_order_update(sender, instance, created, **kwargs):
    if created:
        # Create a default UpdateOrder entry when a new Order is created
        UpdateOrder.objects.create(
            order=instance,
            desc="Order has been placed.",
            status="pending"
        )
