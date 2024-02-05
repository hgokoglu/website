from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout

from .models import Article
from .forms import ArticleForm, CopyBasedArticleForm

def index(request):
	context = {}
	context["news_casters"] = Article.objects.all()
	return render(request = request, template_name = "./index.html", context = context)

def newsfeed(request, news_caster:str):
	context = {}
	dates = Article.objects.order_by("creation_date").values_list("creation_date", flat = True).distinct()[:30]
	articles = [{"date":date, "articles":Article.objects.filter(creation_date = date)} for date in dates]
	articles = sorted(articles, key = lambda item: item["date"], reverse = True)
	context["articles"] = articles
	return render(request = request, template_name = "./newsfeed.html", context = context)

def search(request):
	context = {}
	context["results"] = reversed(Article.objects.filter(title__icontains = request.GET["searched"]))
	return render(request = request, template_name = "./search.html", context = context)

def copy(request):
	context = {}
	if request.method == "POST":
		form = CopyBasedArticleForm(request.POST)
		if form.is_valid():
			copy_article = form.save()
			context["copy_article"] = copy_article
			context["article_text"] = copy_article.text.split("\n")
			return render(request = request, template_name = "./copy.html", context = context)
		else:
			print("Form error", form.errors)
			context["copy_form"] = CopyBasedArticleForm()
	else:
		context["copy_form"] = CopyBasedArticleForm()
	return render(request = request, template_name = "./copy.html", context = context)

def about(request):
	context = {}
	context["login_flag"] = True
	return render(request = request, template_name = "./about.html", context = context)

def login(request):
	context = {}
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return redirect("main:index")
		else:
			print("Credential Error")
	return render(request = request, template_name = "./login.html", context = context)

def logout(request):
	auth_logout(request = request)
	return redirect('main:index')

def article(request, article_id : int):
	context = {}
	article = Article.objects.get(pk = article_id)
	context["article"] = article
	context["article_text"] = article.text.split("\n")
	return render(request = request, template_name = "./article.html", context = context)

def details(request, article_id : int):
	context = {}
	article = Article.objects.get(pk = article_id)
	context["article"] = article
	context["article_text"] = article.text.split("\n")
	if request.method == "POST":
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save(original = article)
			return redirect('main:article', article_id =article.id)
		else:
			print("Try Again")
			context["article_form"] = ArticleForm(initial = article.as_dict())
	else:
		context["article_form"] = ArticleForm(initial = article.as_dict())
	return render(request = request, template_name = "./details.html", context = context)
