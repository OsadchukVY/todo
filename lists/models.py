from django.db import models

# mapping to TABLES in DataBase
class List(models.Model):
    pass

class Item(models.Model):  # mapping to TABLES in DataBase
    text = models.TextField(default='') # large text field
    list = models.ForeignKey(List, default=None)    # relationship between the two classes
