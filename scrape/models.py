from django.db import models


class Tour(models.Model):
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateField(null=True)
    tour_date = models.DateField(null=True)
    author = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    star = models.IntegerField()

    def __str__(self):
        return self.title
