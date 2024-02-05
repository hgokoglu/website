from django import forms
from main.models import Article, CopyBasedArticle

from .api import tts

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ["title", "voice_file"]

	
	def save(self, original, commit = True):
		article = original
		article.title = self.cleaned_data["title"]
		article.voice_file = self.cleaned_data["voice_file"]
		article.updated = True

		if commit:
			article.save()
		
		return article

class CopyBasedArticleForm(forms.ModelForm):
	class Meta:
		model = CopyBasedArticle
		fields = ["text"]
	
	def save(self, commit = True):
		article = CopyBasedArticle(text = self.cleaned_data["text"])
		article.voice_file = tts.to_voice(article.text)

		if commit:
			article.save()
		
		return article
