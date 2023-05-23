from django import forms
from posts.models import Post, PostImage, Comment, Reply


class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post 
		fields = ['content', 'video', 'visibility']

class PostEditForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['content',]

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment',]

class ReplyForm(forms.ModelForm):
	class Meta:
		model = Reply
		fields = ['reply',]

# class SharedPostForm(forms.ModelForm):
# 	class Meta:
# 		model = SharedPost
# 		fields = ['visibility',]