import base64
import pickle

from django.db import models
# Create your models here.

class Map(models.Model):
    map_name = models.CharField(max_length=100)
    
    #_map_instance = models.TextField(db_column='map_instance')
    
    def __str__(self):
        return self.map_name

#    def set_data(self, data):
#        self._data = base64.encodestring(data)
#
#    def get_data(self):
#        return base64.decodestring(self._data)
#
#    data = property(get_data, set_data)
#

class Event(models.Model):
    lon = models.FloatField() 
    lat = models.FloatField() 
    locname = models.TextField()
    title = models.TextField()
    desc = models.TextField()
    catlist = models.TextField()
    starttime = models.TextField()
    endtime = models.TextField()
    timetoann = models.TextField()
    mapid = models.ForeignKey(Map,on_delete=models.CASCADE)
    
    def __str__(self):
        return ("TITLE: " + self.title + "   LOCNAME:   " + self.locname 
        + "  LON: " + self.lon + "  LAT: "+ self.lat +
        + "  STARTTIME: " +  self.starttime + "  ENDTIME: " + self.endtime
        + "  DESC: " + self.desc)
