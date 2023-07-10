from django.db import models
from djongo.models.fields import ObjectIdField

class Search(models.Model):
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

    @classmethod
    def search_by_title(cls, query):
        return cls.objects.filter(ProductTitle__icontains=query)
