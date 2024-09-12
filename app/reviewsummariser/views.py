from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import URL, Summary
from .serializer import SummarySerializer
from . import reviews

@api_view(['GET'])
def get_summary(request):
    url = request.query_params.get('url')
    
    if "amazon" not in url:
        return Response(
            {"error": "Please enter an amazon URL"},
            status=status.HTTP_400_BAD_REQUEST
        )
    summary = reviews.summarise_reviews(url)
    
    if summary == "":
        return Response(
            {"error": "No reviews found"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return Response(SummarySerializer({'summary': summary}).data)