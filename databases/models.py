import uuid
from django.db import models

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # id = models.FloatField()
    title = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.URLField()
    productId=models.FloatField()

    rate = models.FloatField()
    count = models.IntegerField()

    def __str__(self):
        return self.title
