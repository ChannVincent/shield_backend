from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Post
import json

# View to get all posts by commune : http://localhost:8000/posts/?commune_id=0
@require_http_methods(["GET"])
def get_all_posts(request):
    commune_id = request.GET.get('commune_id')
    if not commune_id:
        return JsonResponse({'error': 'commune_id is required'}, status=400)
    try:
        posts = Post.objects.filter(commune_id=commune_id).order_by('-id').values()
        return JsonResponse(list(posts), safe=False) 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    

# View to create a new post : http://localhost:8000/posts/create
@csrf_exempt  # Disable CSRF for this endpoint
@require_http_methods(["POST"])
def create_post(request):
    try:
        # Ensure the request is multipart/form-data
        commune_id = request.POST.get('commune')
        title = request.POST.get('title')
        text = request.POST.get('text')
        json_data = request.POST.get('json_data')  # JSON as a string
        image = request.FILES.get('image')  # Handle the uploaded image

        # Create the post
        new_post = Post.objects.create(
            commune_id=commune_id,
            title=title,
            text=text,
            json_data=json_data,
            image=image
        )

        # Respond with success
        return JsonResponse({'message': 'Post created successfully', 'post_id': new_post.id}, status=201)
    except Exception as e:
        # Handle errors
        return JsonResponse({'error': str(e)}, status=400)


# create automatic post from security data
def auto_post(commune_id):
    pass