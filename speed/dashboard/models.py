from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
	username = models.CharField(max_length=100)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	parent_name = models.ManyToManyField("self", blank=True)
	is_parent = models.BooleanField(default=True)
	phone = models.CharField(max_length=100, blank=True)


	def __str__(self):
		return self.username