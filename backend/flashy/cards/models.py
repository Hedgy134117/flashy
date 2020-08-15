from django.db import models

# Create your models here.
class Card(models.Model):
    group = models.ForeignKey('cards.Set', related_name = 'cards', on_delete = models.CASCADE)
    front = models.TextField(max_length = 500)
    back = models.TextField(max_length = 500)

class Set(models.Model):
    owner = models.ForeignKey('auth.User', related_name = 'sets', on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, default = '')