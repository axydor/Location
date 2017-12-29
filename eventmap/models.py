import base64

from django.db import models

# Create your models here.

class Map(models.Model):
    map_name = models.CharField(max_length=100)
    
    _map_instance = models.TextField(db_column='map_instance')

    def __str__(self):
        return self.map_name

    def set_data(self, data):
        self._data = base64.encodestring(data)

    def get_data(self):
        return base64.decodestring(self._data)

    data = property(get_data, set_data)
