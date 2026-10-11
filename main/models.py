import uuid

from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField('Full plate price', max_digits=6, decimal_places=2)
    half_price = models.DecimalField('Half plate price', max_digits=6, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return self.name

    @property
    def effective_half_price(self):
        return self.half_price
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Order(models.Model):
    class Status(models.TextChoices):
        RECEIVED = 'received', 'Received'
        PREPARING = 'preparing', 'Preparing'
        READY = 'ready', 'Ready'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.RECEIVED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order {self.pk} — {self.customer_name}"


class OrderItem(models.Model):
    class PlateSize(models.TextChoices):
        HALF = 'half', 'Half plate'
        FULL = 'full', 'Full plate'

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    plate_size = models.CharField(max_length=4, choices=PlateSize.choices)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    line_total = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} × {self.item_name} ({self.get_plate_size_display()})"
