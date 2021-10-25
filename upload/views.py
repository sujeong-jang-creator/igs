from django.shortcuts import render

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
from igs import settings
from . import forms
from .apps import UploadConfig
import tensorflow as tf

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
    # 요청파라미터 - text: request.POST, file: request.FILES
    form = forms.UploadForm(request.POST, request.FILES)

    if form.is_valid(): #요청파라미터 검증. True: 검증 성공, False: 검증 실패
        clean_data = form.cleaned_data #Form에서 직접 값을 조회할 수 없다. form.cleaned_data: 검증을 통과한 
                                       #요청파라미터들을 딕셔너리로 반환. 이 딕셔너리를 이용해 조회
        img_field  = clean_data['upimg'] #업로드된 파일을 조회
        print(img_field, type(img_field))
        print(img_field.image.width, img_field.image.height, img_field.image.format, img_field.name) #ImageField.name: 파일명
        
        image = Image.open(img_field) # 이미지 로딩
        image_resize = image.resize((512,512)) #모델 input shape- (150,150,3)
        image_arr = np.array(image_resize) #PIL 이미지 타입을 ndarray 변환
        image_arr = image_arr/255. # 정규화
        input_tensor = image_arr[np.newaxis, ...] #배치 축 추가 (150,150,3) => (1, 150,150,3)

        model = UploadConfig.model
        pred = model.predict(input_tensor) #출력층 activation: sigoid  0:cat, 1:dog  [[0.7]]
        
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
                max_output_size_per_class = 50, # class 별로 최대 몇개의 bbox를 찾을 것인지
                max_total_size = 3, # 전체 bbox를 최대 몇개 찾을 것인지
                iou_threshold = IOU_THRESH, # IoU 임계값
                score_threshold = CONFIDENCE_SORE_THRESH, #confidence score의 임계값 - 이것보다 낮은 학률로 예측된 것은 안나오게 함)
        )

        # 
        # min_y = boxes[0][0][0]
        # min_x = boxes
        # max_y = 
        # max_x = 
        print(boxes[0][0][0])
        print("boxes : ", boxes)
        print("scores : ", scores)
        print("classes : ", classes)
        print("valid detections : ", valid_detections)

        for i in range(valid_detections[0]):
            print(i)

        # save_path = os.path.join(settings.MEDIA_ROOT, img_field.name)
        # print(save_path)
        # image.save(save_path) #PIL Image객체.save(경로) : 이미지 저장.       
        
        return render()