from django.db import models

class userApiConfig(models.Model):
    username = models.CharField(max_length = 255, default = 0)
    name = models.CharField(max_length = 255, default = 0)
    api_key = models.CharField(max_length = 255, default = 0)
    timestamp = models.CharField(max_length = 255, default = 0)

    def __str__(self):
        return self.username
