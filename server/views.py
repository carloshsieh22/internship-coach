from django.http import HttpResponse
import google.generativeai as genai
from .models import Business
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from .models import Business
from django.http import JsonResponse

def business_list_view(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')

    # Filter businesses based on query parameters
    businesses = Business.objects.all()
    if search:
        businesses = businesses.filter(name__icontains=search)
    if category:
        businesses = businesses.filter(category__icontains=category)
    if location:
        businesses = businesses.filter(address__icontains=location)

    # Limit the number of entries to 20
    businesses = businesses[:20]
    print(f"Filtered businesses count: {businesses.count()}")
    return render(request, 'business_list.html', {'businesses': businesses})

genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def index(request):
    return render(request, 'index.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

class MyView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        return Response({'message': 'Hello, anonymous user!'})
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache
@csrf_exempt
def generate(request):
    if request.method == "POST":
        # Use a unique cache key for anonymous users
        cache_key = f"generate_request_{request.META.get('REMOTE_ADDR')}"
        
        # Check if the request has already been made
        if cache.get(cache_key):
            return JsonResponse({'error': 'You have already made a request.'}, status=429)
        
        # Process the request
        preset_prompt = request.POST.get('preset_prompt')
        custom_prompt = request.POST.get('custom_prompt')

        if preset_prompt:
            user_input = preset_prompt
        elif custom_prompt:
            user_input = custom_prompt
        else:
            user_input = None

        if user_input:
            try:
                response = model.generate_content(user_input)
                response_text = response.text
                # Set the cache to expire after a certain time (e.g., 24 hours)
                cache.set(cache_key, True, timeout=360)
                return JsonResponse({'response': response_text})
            except Exception as e:
                return JsonResponse({'error': f"Error generating content: {str(e)}"}, status=500)
        else:
            return JsonResponse({'error': 'Input cannot be empty.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def favicon(request):
    return HttpResponse(status=204)
def generator_view(request):
    return render(request, 'generator.html')
def about(request):
    return render(request, 'about.html')
def priv_terms(request):
    return render(request, 'priv_terms.html')

