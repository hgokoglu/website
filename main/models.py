from django.db import models
from django.utils.timezone import now

class Article(models.Model):
	title = models.CharField(max_length = 256, default = "", blank = True)		# Title of the article
	text = models.TextField(max_length = 8192, null = False, blank = False)		# Main body of the article
	news_caster = models.CharField(max_length = 64, default = "")			# Publisher
	link = models.CharField(max_length = 512, default = "", blank = True)		# Link to the original
	category = models.CharField(max_length = 32, default = "", blank = True)	# Respective category of the article
	creation_date = models.DateField(default = now, null = False)			# Date of creation
	voice_file = models.FileField(blank = True)									# Voice over sound file
	updated = models.BooleanField(default = False)								# Updated with VA file

	def __str__(self) -> str:
		return self.title
	
	def as_dict(self) -> dict:
		to_return = {}
		to_return["title"] = self.title
		to_return["text"] = self.text
		to_return["link"] = self.link
		to_return["category"] = self.category
		to_return["voice_file"] = self.voice_file
		return to_return

class CopyBasedArticle(models.Model):
	text = models.TextField(max_length = 8192, null = False, blank = False)		# Main body of the article
	voice_file = models.FileField(blank = True)									# Voice over sound file
	creation_date = models.DateTimeField(default = now, null = False)			# Date and Time of creation

	def __str__(self) -> str:
		return self.text[:30]