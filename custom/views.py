import base64
from PIL import Image 
import torch
from django.shortcuts import render
from .forms import ImageUploadForm
import os
import cv2
import torch
from ultralytics import YOLO
import io

def detect_objects(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']

            img_path = os.path.join('media', 'uploads', image.name)
            with open(img_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            weights_path = 'best.pt'  
            
            yolo = YOLO(weights_path)
            detection = yolo.predict(img_path,conf=0.4,save=True)
            
            
            folder_path = 'runs/detect/'
            subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
            latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
            img_path = folder_path+'/'+latest_subfolder+'/'+image.name
            
            
            with open(img_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            return render(request, 'result.html', {'encoded_image': encoded_image})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

  
    