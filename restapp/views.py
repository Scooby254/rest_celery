from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import process_image
from .models import ProcessedImage

@api_view(['POST'])
def process_request_view(request):
    image_url = request.data.get('image_url')
    result = process_image.delay(image_url)
    print("Request successful, doing image processing in the background!!!")
    return Response({'task_id': result.id})


""" @api_view(['GET'])
def get_processed_images(request):
    processed_images = ProcessedImage.objects.all()
    serialized_data = [
        {
            'original_image': processed.original_image.url,
            'processed_image': processed.processed_image.url,
            'timestamp': processed.timestamp
        }
        for processed in processed_images
    ]
    
    return Response(serialized_data) """