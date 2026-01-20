from django.db import models
from django.utils.text import slugify

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField(max_length=200,null=True,blank=True)
    is_active = models.BooleanField(default=True)



class Products(models.Model):
    name = models.CharField(max_length=100,default=f'Product-{id}',blank=True)
    desc = models.TextField(max_length=200,null=True)
    slug = models.SlugField(max_length=255,unique=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='products')
    stock_left = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args , **kwargs):
        if not self.slug:
            base_slug = self.slug
            slug = base_slug
            count = 1

            while Products.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count+=1

        return super().save(*args, **kwargs)
    


