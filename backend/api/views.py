from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def greet_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text', '')
        if text == 'こんにちは':
            return JsonResponse({'response': 'Hello'})
        else:
            return JsonResponse({'response': 'Unknown greeting'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
