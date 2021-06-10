from django.db import models

# Create your models here.
class Accounts(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    def __str__(self):
        return self.username

class Characters(models.Model):
    owner = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=30)
    def __str__(self):
        return self.character_name

class Skills(models.Model):
    character = models.ForeignKey(Characters, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=20)
    results = models.CharField(max_length=50)
    def __str__(self):
        return self.skill_name
