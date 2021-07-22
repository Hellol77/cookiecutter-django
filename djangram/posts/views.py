from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request,'posts/base.html')

def post_create(request):
	if request.method=='GET':
		return render(request, 'post/base.html')
	elif request.method=='POST':
		pass