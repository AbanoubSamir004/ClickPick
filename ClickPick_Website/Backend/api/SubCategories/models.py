from django.db import models
from djongo.models.fields import ObjectIdField

class SubCatQuerySet(models.QuerySet):
    def with_subcategory(self, subcategory):
        return self.filter(ProductSubCategory=subcategory)

class SubCatManager(models.Manager):
    def get_queryset(self):
        return SubCatQuerySet(self.model, using=self._db)

    def with_subcategory(self, subcategory):
        return self.get_queryset().with_subcategory(subcategory)

class SubCat(models.Model):
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


    objects = SubCatManager()

    def __str__(self):
        return self.ProductTitle
