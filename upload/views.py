from django.shortcuts import redirect, render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

# from upload.forms import PickPhotoForm
# from upload.models import PickPhoto

import os
import json
import numpy as np
from PIL import Image
from django.http import HttpResponse
from numpy.lib.npyio import save
from igs import settings
from . import forms
from .apps import UploadConfig
import tensorflow as tf
from upload.models import Results
from account.models import User
import uuid

# class PickPhotoView(CreateView):
#     model = PickPhoto
#     context_object_name = 'pick_photo'
#     form_class = PickPhotoForm
#     success_url = reverse_lazy('account:hello_world')
#     template_name = 'upload/pick_photo.html'

    # def form_valid(self, form):
    #     temp_pick_photo = form.save(commit=False)
    #     temp_pick_photo.user = self.request.user
    #     temp_pick_photo.save()
    #
    #     return super().form_valid(form)


def predict(request):
    form = forms.UploadForm(request.POST, request.FILES)

    if form.is_valid(): 
        clean_data = form.cleaned_data 
        img_field  = clean_data['upimg']
        print(img_field, type(img_field))
        print(img_field.image.width, img_field.image.height, img_field.image.format, img_field.name) 
        
        image = Image.open(img_field) 
        image_resize = image.resize((512,512)) 
        image_arr = np.array(image_resize) 
        image_arr = image_arr/255. 
        input_tensor = image_arr[np.newaxis, ...] 

        model = UploadConfig.model
        pred = model.predict(input_tensor) 
        
        print("pred : " , pred)
        print("--------------------")
        # 후처리
        pred_boxes = pred[:,:, :4] # 예측한 bbox 좌표
        pred_conf = pred[:, :, 4:] # 예측한 class 별 확률
        
        tf.reshape(pred_boxes, (tf.shape(pred_boxes)[0], -1, 1, 4)).shape
        tf.reshape(pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])).shape

        IOU_THRESH = 0.2
        CONFIDENCE_SORE_THRESH = 0.2

        boxes, scores , classes, valid_detections = tf.image.combined_non_max_suppression(
                boxes = tf.reshape(pred_boxes, (tf.shape(pred_boxes)[0], -1, 1, 4)), # bbox 좌표 추론값
                scores = tf.reshape(pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                max_output_size_per_class = 50, 
                max_total_size = 3, 
                iou_threshold = IOU_THRESH, 
                score_threshold = CONFIDENCE_SORE_THRESH, 
        )

        # Result 모델에 들어갈 내용 찾기
        min_y = boxes[0][0][0]
        min_x = boxes[0][0][1]
        max_y = boxes[0][0][2]
        max_x = boxes[0][0][3]

        for i in range(len(pred[0])):
            print(pred[0][i][0], pred[0][i][1], pred[0][i][2], pred[0][i][3])
            if pred[0][i][0] == min_y and pred[0][i][1] == min_x and pred[0][i][2] == max_y and pred[0][i][3]==max_x:
                class_prob = [pred[0][i][4], pred[0][i][5], pred[0][i][6], pred[0][i][7], pred[0][i][8]]
                # print(class_prob)
                break      
        
        sorted_index = np.argsort(class_prob)
        # print(sorted_index)
        # print(class_prob)
        class_str = ["1++", "1+", "1", "2", "3"]
        # save_path = os.path.join(settings.MEDIA_ROOT, img_field.name)
        print("settings.MEDIA_ROOT : ", settings.MEDIA_ROOT)
        print("MEDIA_URL : ", settings.MEDIA_URL)
        
        user = User(pk=request.user.pk)
        print(user)
    
        result = Results(img_file_path = '/media/',  first_grade=class_str[sorted_index[4]], 
        first_grade_percentage = int(np.round(100*class_prob[sorted_index[4]])), second_grade = class_str[sorted_index[3]], 
        second_grade_percentage = int(np.round(100*class_prob[sorted_index[3]])), third_grade = class_str[sorted_index[2]], 
        third_grade_percentage = int(np.round(100*class_prob[sorted_index[2]])), user_id= user)
        result.save()

        save_path = os.path.join('/media/', str(result.pk))
        save_path = save_path + '.' + img_field.name.split('.')[-1]
        result.img_file_path=save_path
        result.save()

        save_path = os.path.join(settings.MEDIA_ROOT, str(result.pk))
        save_path = save_path + '.' + img_field.name.split('.')[-1]
        print("새로만든 save_path : ", save_path)
        print("img_filed.name : ", img_field.name)
        img_field.name = str(result.pk)
        print("img_filed.name : ", img_field.name)

        image.save(save_path, format=None)
                
        return redirect(f'/result/show_result/{result.pk}')