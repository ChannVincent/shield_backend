from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from security_data.models import *
import json
from django.core import serializers
import wikipediaapi
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count


# View to get all posts by commune : http://localhost:8000/posts/?commune_id=0
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    """
    API view to return all posts for the authenticated user's commune.
    Each post includes the number of comments.
    """
    user = request.user
    commune_id = user.commune.pk

    if not commune_id:
        return JsonResponse({'error': 'commune_id is required'}, status=400)

    try:
        # Automate posts and retrieve data
        auto_post_general_info(commune_id=commune_id)
        auto_post_security(commune_id=commune_id)

        # Retrieve posts with related user and comment data
        posts = Post.objects.filter(commune_id=commune_id).prefetch_related(
            'user',  # Fetch the post creator user
            'likes'  # Fetch users who liked the post
        ).annotate(comment_count=Count('comments')).order_by('-id')

        formatted_posts = []
        for post in posts:
            post_data = {
                'id': post.pk,
                'commune_id': post.commune_id,
                'title': post.title,
                'text': post.text,
                'type': post.type,
                'image': post.image.url if post.image else None,
                'color': post.color,
                'json_data': post.json_data,
                'user_username': post.user.username if post.user else None,
                'user_image': post.user.image.url if post.user and post.user.image else None,
                'user_id': post.user.pk if post.user else None,
                'user_rank': post.user.role if post.user else None,
                'like_count': post.likes.count(),
                'is_liked': request.user in post.likes.all(),
                'comment_count': post.comment_count
            }

            formatted_posts.append(post_data)

        return JsonResponse(formatted_posts, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    

# View to create a new post : http://localhost:8000/posts/create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    try:
        user = request.user
        commune_id = request.user.commune.pk
        text = request.POST.get('text')
        json_data = request.POST.get('json_data') 
        image = request.FILES.get('image')  # Handle the uploaded image

        # Create the post
        new_post = Post.objects.create(
            user=user,
            commune_id=commune_id,
            title=None,
            text=text,
            json_data=json_data,
            image=image
        )

        # Respond with success
        return JsonResponse({'message': 'Post created successfully', 'post_id': new_post.id}, status=201)
    except Exception as e:
        # Handle errors
        return JsonResponse({'error': str(e)}, status=400)



# View to like or unlike post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)

    # Check if the user already liked the post
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)  # Unlike the post
        liked = False
    else:
        post.likes.add(user)  # Like the post
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': post.likes.count(),
    })



# View to add a comment to a specific post.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_comment(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)

    # Extract the comment text from the request
    text = request.data.get('text', '').strip()
    if not text:
        return JsonResponse({'error': 'Comment text cannot be empty.'}, status=400)

    # Create the comment
    comment = Comment.objects.create(user=user, post=post, text=text)

    return JsonResponse({
        'id': comment.id,
        'user': comment.user.username if comment.user else None,
        'text': comment.text,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
    }, status=201)



# View to get all comments for a specific post
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')

    # Serialize the comments
    comments_data = [
        {
            'id': comment.id,
            'user': comment.user.username if comment.user else None,
            'user_id': comment.user.pk if comment.user else None,
            'user_rank': comment.user.role if comment.user else None,
            'user_image': comment.user.image.url if (comment.user and comment.user.image) else None,
            'from_me': comment.user.pk == user.pk if comment.user else False,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': comment.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for comment in comments
    ]

    return JsonResponse({'comments': comments_data}, status=200)



# Create automatic post from security data
def auto_post_security(commune_id):
    commune = Commune.objects.get(pk=commune_id)
    
    aggression_class_list = [
        ("Usage de stupéfiants", "#f80d09"), 
        ("Trafic de stupéfiants", "#f80d09"),
        ("Destructions et dégradations volontaires", "#000000"), 
        ("Cambriolages de logement", "#000000"),
        ("Violences sexuelles", "#cd09f8"),
    ]
    posts = []
    for aggression in aggression_class_list:
        aggression_class = aggression[0]
        post_exist = Post.objects.filter(commune_id=commune_id, type=aggression_class).first()
        if post_exist:
            continue
        color = aggression[1]
        title = aggression_class + " à " + commune.name_full
        securite_records = Securite.objects.filter(commune_id=commune_id, agression_class=aggression_class)
        # Convert to simplified JSON format
        simplified_securite_data = [
            {
                "commune": record.commune.pk,
                "year": record.year,
                "agression_class": record.agression_class,
                "aggression_unity": record.aggression_unity,
                "facts_value": "0" if record.facts_value == "NA" else record.facts_value,
            }
            for record in securite_records
        ]
        # Convert to JSON
        securite_json = json.dumps(simplified_securite_data)
        # Create a new post
        new_post = Post.objects.create(
            commune_id=commune_id,
            title=title,
            text=None,
            color=color,
            json_data=securite_json,
            type=aggression_class,
        )
        posts.append(new_post)

    return posts



# Create automatic post from wiki
def auto_post_general_info(commune_id):
    commune = Commune.objects.get(pk=commune_id)
    wiki_api = wikipediaapi.Wikipedia('shield (ad@min.com)', 'fr')
    # if page wiki of full name commune doesn't exist : return
    page_wiki = wiki_api.page(commune.name_full)
    if not page_wiki.exists():
        return
    post_type_summary = "wiki_summary"
    post_type_location = "wiki_location"
    post_type_road = "wiki_road"
    post_type_transport = "wiki_transport"
    # post summary
    post_summary = Post.objects.filter(commune_id=commune_id, type=post_type_summary).first()
    if post_summary == None:
        Post.objects.create(
            commune_id=commune_id,
            title=commune.name_full,
            text=page_wiki.summary,
            type=post_type_summary
        )
    # sections
    for section in page_wiki.sections:
        if section.title == "Géographie":
            for sub_section in section.sections:
                if sub_section.title == "Localisation":
                    # post location
                    post_location = Post.objects.filter(commune_id=commune_id, type=post_type_location).first()
                    if post_location == None:
                        Post.objects.create(
                            commune_id=commune_id,
                            title=sub_section.title,
                            text=sub_section.text,
                            type=post_type_location
                        )

        if section.title == "Urbanisme":
            for sub_section in section.sections:
                if sub_section.title == "Voies de communications et transports":
                    for sub_sub_section in sub_section.sections:
                        if sub_sub_section.title == "Voies routières":
                            # post road
                            post_road = Post.objects.filter(commune_id=commune_id, type=post_type_road).first()
                            if post_road == None:
                                Post.objects.create(
                                    commune_id=commune_id,
                                    title=sub_sub_section.title,
                                    text=sub_sub_section.text,
                                    type=post_type_road
                                )
                                
                        if sub_sub_section.title == "Transports en commun":
                            # post transport
                            post_transport = Post.objects.filter(commune_id=commune_id, type=post_type_transport).first()
                            if post_transport == None:
                                Post.objects.create(
                                    commune_id=commune_id,
                                    title=sub_sub_section.title,
                                    text=sub_sub_section.text,
                                    type=post_type_transport
                                )
        
        
                

