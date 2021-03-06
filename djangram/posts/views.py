from djangram.posts import serializers
from django.shortcuts import get_object_or_404, render
from djangram.users.models import User as user_model
from . import models
from django.db.models import Q
from .forms import CreatePostForm
from django.contrib.auth import logout
from django.http.response import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def index(request):
	if request.method == "GET":
		if request.user.is_authenticated:
			user = get_object_or_404(user_model,pk=request.user.id)
			following = user.following.all()
			posts = models.Post.objects.filter(
				Q(author__in=following) | Q(author=user)
			)
						
			serializer = serializers.PostSerializer(posts,many=True)
			print(serializer.data)
			return render(request,'posts/main.html',{"posts": serializer.data})
			
			


def post_create(request):
	if request.method=='GET':
		form =CreatePostForm()
		return render(request, 'posts/post_create.html', {"form":form})
		
	elif request.method=='POST':
		if request.user.is_authenticated:
			user = get_object_or_404(user_model, pk=request.user.id)
			# image = request.FILES['image']
			# caption = request.POST['caption']
			
			# new_post = models.Post.objects.create(
			# 	author = user,
			# 	image = image,
			# 	caption = caption
			# )
			# new_post.save()
			
			form = CreatePostForm(request.POST, request.FILES)
			if form.is_valid():
				post = form.save(commit=False)
				post.author = user
				post.save()
			else:
				print(form.errors)
			user = get_object_or_404(user_model,pk=request.user.id)
			following = user.following.all()
			posts = models.Post.objects.filter(
				Q(author__in=following) | Q(author=user)
			)
					
			serializer = serializers.PostSerializer(posts,many=True)
			return render(request,'posts/main.html',{"posts": serializer.data})
		else:
			return render(request,'users/main.html')
			

