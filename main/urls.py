from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", view = views.index, name = "index"),
	path("newsfeed/<str:news_caster>", view = views.newsfeed, name = "newsfeed"),
	path("search/", view = views.search, name = "search"),
	path("copy/", view = views.copy, name = "copy"),
	path("article/<int:article_id>/", view = views.article, name = "article"),
	path("about/", view = views.about, name = "about"),
	path("login/", view = views.login, name = "login"),
    path("logout", view = views.logout, name = "logout"),
    path("details/<int:article_id>/", view = views.details, name = "details")
]