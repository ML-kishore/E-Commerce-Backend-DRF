from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200,blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Categories.objects.filter(slug=slug).exists():
                base_slug = f"{base_slug}--{counter}"
                counter+=1

            self.slug = slug

        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name



class Products(models.Model):

    #Todo add seperate model for ratings because ratings is a user input fields and we shoould build it like user rated and average rated value to this model .....

    
    name = models.CharField(max_length=100,default=f'Product-{id}',blank=True)
    desc = models.TextField(max_length=200,blank=True)
    slug = models.SlugField(max_length=255,unique=True,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='products')
    stock_left = models.PositiveIntegerField()
    ratings = models.IntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(5)])
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    def save(self, *args , **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1

            while Products.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count+=1

            self.slug = slug 

        return super().save(*args, **kwargs)
    

    
    def __str__(self):
        return self.name
