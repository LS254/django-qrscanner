from django.db import models

class ScannedCodes(models.Model):
    qr_code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    scanned_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name