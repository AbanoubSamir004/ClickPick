from django.db import models
from djongo.models.fields import ObjectIdField


class SalesQuerySet(models.QuerySet):
    def with_product_offer(self):
        return self.exclude(ProductOldPrice='')

class SalesManager(models.Manager):
    def get_queryset(self):
        return SalesQuerySet(self.model, using=self._db).with_product_offer()


class Sales(models.Model):
    _id = ObjectIdField()
    Marketplace= models.CharField(max_length=255)
    ProductTitle = models.CharField(max_length=255)
    ProductBrand = models.CharField(max_length=255)
    ProductCategory = models.CharField(max_length=255)
    ProductDescription = models.TextField()
    ProductID = models.CharField(max_length=255)
    ProductImage = models.URLField()
    ProductLink = models.URLField()
    ProductOldPrice = models.CharField(max_length=255)
    ProductPrice = models.CharField(max_length=255)
    ProductRatingCount = models.CharField(max_length=255)
    ProductRatings = models.CharField(max_length=255)
    ProductSpecifications =models.CharField(max_length=255)
    ProductSubCategory = models.CharField(max_length=255)
    SellerName = models.CharField(max_length=255)
    SellerUrl = models.URLField()
    ProductMatchingIDs =models.CharField(max_length=255)
    ProductSentimentAnalysis =models.CharField(max_length=255)
    SellerSentimentAnalysis =models.CharField(max_length=255)
    ProductAspects =models.CharField(max_length=255)


    class Meta:
        managed = False
        db_table = 'Products_Collection'


    objects = SalesManager()

    def __str__(self):
        return self.ProductTitle
