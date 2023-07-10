from django.db import models
from djongo.models.fields import ObjectIdField

class Promotion(models.Model):
    _id = ObjectIdField()
    PromotionID =  models.CharField(max_length=255)
    Marketplace = models.CharField(max_length=255)
    PromotionsTitle = models.CharField(max_length=255)
    PromotionsCoupon = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Promotions_Collection'

    def __str__(self):
        return self.PromotionsTitle
