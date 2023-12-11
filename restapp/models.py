from django.db import models

def upload_original_path(instance, filename):
    path = f'original_images/{filename}'
    print(f"Original Image Path: {path}")
    return path

def upload_processed_path(instance, filename):
    path = f'processed_images/{filename}'
    print(f"Processed Image Path: {path}")
    return path

class ProcessedImage(models.Model):
    original_image = models.ImageField(upload_to=upload_original_path)
    processed_image = models.ImageField(upload_to=upload_processed_path)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_image.name} - {self.timestamp}"