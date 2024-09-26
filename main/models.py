from django.db import models
from django.contrib.auth.models import User
import string,random

class links(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    short_link = models.CharField(max_length=6,unique=True, null=True, blank=True)
    link = models.TextField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    no_of_views = models.PositiveIntegerField(default=0)

    def generate_id(self):
        characters = string.ascii_letters + string.digits
        while True:
            random_string = ''.join(random.choices(characters, k=5))
            if not links.objects.filter(short_link=random_string).exists():
                return random_string
    
    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = self.generate_id()    
        super(links, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f'{self.name}-{self.link}'   
        
class link_history(models.Model):
    link = models.ForeignKey(links,on_delete=models.DO_NOTHING)
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    
    user_agent = models.CharField(max_length=300, null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)
    
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    isp = models.CharField(max_length=200, null=True, blank=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    device = models.CharField(max_length=100, null=True, blank=True)
    device_brand = models.CharField(max_length=100, null=True, blank=True)
    device_model = models.CharField(max_length=100, null=True, blank=True)
    
    os = models.CharField(max_length=100, null=True, blank=True)
    os_version = models.CharField(max_length=100, null=True, blank=True)
    
    browser = models.CharField(max_length=100, null=True, blank=True)
    browser_version = models.CharField(max_length=100, null=True, blank=True)
    
    screen_resolution = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.link}={self.ip}'