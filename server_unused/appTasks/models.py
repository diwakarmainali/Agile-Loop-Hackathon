from django.db import models
from authentication.models import UserAccount
# Create your models here.
class App(models.Model):
    app_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='app_images/')
    points = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='created_apps')

    def __str__(self):
        return self.app_name

class CompletedTask(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='completed_tasks')
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='completed_tasks')
    screenshot = models.ImageField(upload_to='screenshots/')
    date_completed = models.DateTimeField(auto_now_add=True)
    VERIFIED_CHOICES = (
        (False, 'No'),
        (True, 'Yes'),
    )
    verified = models.BooleanField(choices=VERIFIED_CHOICES, default=False)

    

    def __str__(self):
        return f"{self.user.email} - {self.app.app_name}"
