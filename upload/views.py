from django.shortcuts import redirect, render

import os
import json
import numpy as np
from PIL import Image
from django.http import HttpResponse
# from numpy.lib.npyio import save
from igs import settings
from . import forms
from .apps import UploadConfig
import tensorflow as tf
from upload.models import Results
from account.models import User

def predict(request):
    form = forms.UploadForm(request.POST, request.FILES)

    if form.is_valid(): 
        clean_data = form.cleaned_data 
        img_field  = clean_data['upimg']
        # print(img_field, type(img_field))
        # print(img_field.image.width, img_field.image.height, img_field.image.format, img_field.name) 
        
        image = Image.open(img_field) 
        image_resize = image.resize((512,512)) 
        image_arr = np.array(image_resize) 
        image_arr = image_arr/255. 
        input_tensor = image_arr[np.newaxis, ...] 

        model = UploadConfig.model
        pred = model.predict(input_tensor) 
        
        if len(pred[0]) == 0: # 사진의 화질이 좋지 않아서 검출이 되지 않는 경우
            return redirect('/upload/error_page')

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

        print("boxes : ", boxes)
        print("boxlen : ", len(boxes[0]))

        # Result 모델에 들어갈 내용 찾기
        min_y = boxes[0][0][0]
        min_x = boxes[0][0][1]
        max_y = boxes[0][0][2]
        max_x = boxes[0][0][3]

        # box의 위치 찾기를 실패하는 경우 에러 페이지 연결
        flag = True

        for i in range(len(pred[0])):
            print(pred[0][i][0], pred[0][i][1], pred[0][i][2], pred[0][i][3])
            if pred[0][i][0] == min_y and pred[0][i][1] == min_x and pred[0][i][2] == max_y and pred[0][i][3]==max_x:
                class_prob = [pred[0][i][4], pred[0][i][5], pred[0][i][6], pred[0][i][7], pred[0][i][8]]
                flag = False
                break    
        
        if flag:
            return redirect('/upload/error_page')     
        

        sorted_index = np.argsort(class_prob)
        class_str = ["1++", "1+", "1", "2", "3"]
        # print("settings.MEDIA_ROOT : ", settings.MEDIA_ROOT)
        # print("MEDIA_URL : ", settings.MEDIA_URL)
        
        user = User(pk=request.user.pk)
        # print(user)
    
        # Result에 모델 저장
        result = Results(img_file_path = '/media/',  first_grade=class_str[sorted_index[4]], 
        first_grade_percentage = int(np.round(100*class_prob[sorted_index[4]])), second_grade = class_str[sorted_index[3]], 
        second_grade_percentage = int(np.round(100*class_prob[sorted_index[3]])), third_grade = class_str[sorted_index[2]], 
        third_grade_percentage = int(np.round(100*class_prob[sorted_index[2]])), user_id = user)
        result.save()
       
        # Result 이미지 경로 수정 

        print(result.pk)
        save_path = os.path.join('/media/', str(result.pk))
        save_path = save_path + '.' + img_field.name.split('.')[-1]
        result.img_file_path=save_path
        result.save()

        # 새로 만든 이미지 이름으로 media 폴더에 이미지 저장

        if not os.path.isdir(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        save_path = os.path.join(settings.MEDIA_ROOT, str(result.pk))
        save_path = save_path + '.' + img_field.name.split('.')[-1]
        image.save(save_path, format=None)


        # 재학습을 위한 image, text 정보 저장

        center_x = (min_x + max_x)/2
        center_y = (min_y + max_y)/2

        object_width = (max_x - min_x)
        object_height = (max_y - min_y)

        label = sorted_index[4]

        DATASET_SAVE_PATH = 'dataset'
        if not os.path.isdir(DATASET_SAVE_PATH):
            os.makedirs(DATASET_SAVE_PATH)

        text_name = str(result.pk) + ".txt"
        image_name = str(result.pk) + '.' + img_field.name.split('.')[-1]
        img_field.name = image_name

        TEXT_SAVE_PATH = os.path.join(DATASET_SAVE_PATH, text_name)
        IMG_SAVE_PATH = os.path.join(DATASET_SAVE_PATH, image_name)

        with open(TEXT_SAVE_PATH, 'wt') as fw:
            save_str = f"{label} {center_x} {center_y} {object_width} {object_height}" 
            fw.writelines(save_str)
            
        image.save(IMG_SAVE_PATH, format=None)
        
        return redirect(f'/result/show_result/{result.pk}')

def error_page(request):
    return render(request, 'upload/error_page.html')
