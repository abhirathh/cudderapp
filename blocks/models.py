from django.db import models

class userApiConfig(models.Model):
    username = models.CharField(max_length = 255, default = 0)
    broker = models.CharField(max_length = 255, default = 0)
    broker_user_id = models.CharField(max_length = 255, default = 0)
    broker_api_key = models.CharField(max_length = 255, default = 0)
    broker_secret_key = models.CharField(max_length = 255, default = 0)

    def __str__(self):
        return self.username + ' - ' + self.broker
