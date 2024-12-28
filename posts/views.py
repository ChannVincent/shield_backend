from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Post
import json

# View to get all posts by commune : http://localhost:8000/posts/?commune_id=0
@require_http_methods(["GET"])
def get_all_posts(request):
    commune_id = request.GET.get('commune_id')  # Get 'commune_id' from query parameters
    if not commune_id:
        return JsonResponse({'error': 'commune_id is required'}, status=400)
    try:
        posts = Post.objects.filter(commune_id=commune_id).values()  # Filter posts by commune_id
        return JsonResponse(list(posts), safe=False)  # Convert to JSON and return
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

# View to create a new post : http://localhost:8000/posts/create
@csrf_exempt  # Disable CSRF for this endpoint
@require_http_methods(["POST"])
def create_post(request):
    try:
        data = json.loads(request.body.decode('utf-8'))  # Parse JSON body
        new_post = Post.objects.create(
            commune_id=data.get('commune'),  # Assumes the commune ID is provided
            title=data.get('title'),
            text=data.get('text'),
            json_data=data.get('json_data')
        )
        return JsonResponse({'message': 'Post created successfully', 'post_id': new_post.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
