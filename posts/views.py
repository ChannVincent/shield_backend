from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Post
from security_data.models import *
import json
from django.core import serializers

# View to get all posts by commune : http://localhost:8000/posts/?commune_id=0
@require_http_methods(["GET"])
def get_all_posts(request):
    commune_id = request.GET.get('commune_id')
    if not commune_id:
        return JsonResponse({'error': 'commune_id is required'}, status=400)
    try:
        auto_post(commune_id=commune_id)
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
    saved_posts_count = Post.objects.filter(commune_id=commune_id).count()
    if saved_posts_count > 0:
        return
    
    # 1st class: Usage de stupéfiants
    posts = []
    aggression_class = "Usage de stupéfiants"
    commune = Commune.objects.get(pk=commune_id)
    title = aggression_class + " à " + commune.name_full
    securite_records = Securite.objects.filter(commune_id=commune_id, agression_class=aggression_class)
    
    # Convert to simplified JSON format
    simplified_securite_data = [
        {
            "commune": record.commune.pk,
            "year": record.year,
            "agression_class": record.agression_class,
            "aggression_unity": record.aggression_unity,
            "public_value": record.public_value,
            "facts_value": record.facts_value,
            "per_thousand": record.per_thousand,
            "pop": record.pop,
            "millpop": record.millpop,
        }
        for record in securite_records
    ]
    
    # Convert to JSON
    securite_json = json.dumps(simplified_securite_data)
    
    # Create a new post
    new_post = Post.objects.create(
        commune_id=commune_id,
        title=title,
        text=title,
        json_data=securite_json,
    )
    
    posts.append(new_post)
    return posts
