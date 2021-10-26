from django.db import models
from account.models import User

class Results(models.Model):
    # result_id = models.IntegerField(primary_key=True)
    register_date = models.DateField(auto_now_add=True)
    img_file_path = models.TextField(null=False)
    first_grade = models.CharField(max_length=4, null=False)
    first_grade_percentage = models.IntegerField(null=False)
    second_grade = models.CharField(max_length=4, null=False)
    second_grade_percentage = models.IntegerField(null=False)
    third_grade = models.CharField(max_length=4, null=False)
    third_grade_percentage = models.IntegerField(null=False)
    modified_grade = models.CharField(max_length=4, null=True, blank=True)
    # cow_sex = models.CharField(max_length=4, null=True, blank=True)
    # model_id = models.ForeignKey(to=Models, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.pk)
