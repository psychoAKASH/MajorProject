from django.db import models

# Create your models here.
class Data(models.Model):
    data_id = models.AutoField(primary_key=True)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    pH = models.FloatField()
    rainfall = models.FloatField()
    crop_result = models.CharField(max_length=50)
    def __str__(self):
        return self.data_id,self.crop_result


class Feedback_form(models.Model):
    form_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(default="")
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    
