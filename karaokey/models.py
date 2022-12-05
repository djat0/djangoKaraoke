from django.db import models


class Song(models.Model):
    videoId = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=100)
    ytChannel = models.CharField(max_length=100)
    imgSrc = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.videoId} - {self.title}'
