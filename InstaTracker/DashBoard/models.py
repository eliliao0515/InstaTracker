from django.db import models
import json

# Create your models here.
class profile(models.Model):
    Id = models.AutoField(primary_key=True)
    userID = models.CharField(max_length=255, default=None)
    username = models.CharField(max_length=255)
    followers = models.TextField(blank=True)
    followings = models.TextField(blank=True)

    def set_my_list(self, follower, following):
        self.followers = json.dumps(follower)
        self.followings = json.dumps(following)

    def get_my_list(self):
        return [json.loads(self.followers) if self.followers else [],
                json.loads(self.followings) if self.followings else []]
    
    def __str__(self):
        return "username:{} ; id:{}".format(self.username, self.userID)