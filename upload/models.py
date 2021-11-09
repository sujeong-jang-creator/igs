from django.db import models
from account.models import User

class Results(models.Model):
    register_date = models.DateField(auto_now_add=True)
    img_file_path = models.TextField(null=False)
    first_grade = models.CharField(max_length=4, null=False)
    first_grade_percentage = models.IntegerField(null=False)
    second_grade = models.CharField(max_length=4, null=False)
    second_grade_percentage = models.IntegerField(null=False)
    third_grade = models.CharField(max_length=4, null=False)
    third_grade_percentage = models.IntegerField(null=False)
    modified_grade = models.CharField(max_length=4, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['-register_date']