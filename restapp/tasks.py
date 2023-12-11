from celery import shared_task
from PIL import Image
import os
import rembg
import requests
from io import BytesIO
import cv2
import numpy as np
from django.core.files import File
from .models import ProcessedImage

@shared_task
def process_image(image_url):
    # Download the image from the URL
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # Use BytesIO to handle the image data
        image_data = BytesIO(response.content)
        
        try:
            # Attempt to open the image using PIL
            original_image = Image.open(image_data)
            #get the file extension of the file/image
            file_extension = image_url.split('.')[-1].lower()
            
            # Perform background removal, resizing, and conversion
            processed_image = remove_background(original_image)
            #processed_image = resize_image(processed_image)
            processed_image = convert_image(processed_image)

            print("Finished all processing!!!")

            # Save the processed image
            processed_image_path = f'media/processed_images/{image_url.split("/")[-1]}'
            print(processed_image_path)
            os.makedirs(os.path.dirname(processed_image_path), exist_ok=True)
            processed_image.save(processed_image_path)
            print("Saved the image!!!")
            # Save the processed image path to the database
            processed_image_obj = ProcessedImage.objects.create(
                original_image=File(image_data, name=image_url.split("/")[-1]),
                processed_image=processed_image_path,
            )
            print("Image object created!!!")
            return processed_image_obj.id
        except Exception as e:
            print(f"Error processing image: {e}")
            # Log the response content to help diagnose the issue
            #print(f"Response content: {response.content}")
            return None
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return None

def remove_background(image):
    print("Start image processing!!!")
    img_array = np.array(image)
    result = rembg.remove(img_array)
    result_image = Image.fromarray(result)

    print("Removed background successfully!!")

    return result_image

def resize_image(image):
    new_size = (200, 200)
    resized_image  = image.resize(new_size)

    print("Resized image to 200*200")
    return resized_image

def convert_image(image):
    converted_image = image.convert('RGB')
    print("Converted the image to JPG")
    return converted_image
