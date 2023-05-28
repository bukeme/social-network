from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.generic import TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms.models import model_to_dict
from django.http import JsonResponse
from posts.forms import PostCreateForm, PostEditForm, CommentForm, ReplyForm
from posts.models import PostImage, Post, Comment, Reply
from posts.utils import get_feeds_queryset
from posts.decorators import AjaxRequiredOnlyMixin
from groups.models import CustomGroup

# Create your views here.

class HomePageView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
	template_name = 'posts/home.html'
	group = None

	def dispatch(self, request, *args, **kwargs):
		if kwargs.get('group_pk'):
			self.group = CustomGroup.objects.get(pk=kwargs['group_pk'])
		return super().dispatch(request, *args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		# context['posts'] = Post.objects.filter(
		# 	Q(visibility='public') | Q(user=self.request.user)
		# ).order_by('-created')
		context['posts'] = get_feeds_queryset(self.request)
		context['page'] = 'home'
		return context

	def post(self, request, *args, **kwargs):
		post_form = PostCreateForm(request.POST, request.FILES)
		if post_form.is_valid():
			post_form = post_form.save(commit=False)
			post_form.user = request.user
			print('hello')
			if self.group:
				post_form.group = self.group
				post_form.visibility = 'public'
			try:
				post_form.shared_post = Post.objects.get(pk=kwargs['post_pk'])
			except:
				pass
			post_form.save()
			images = request.FILES.getlist('images')
			if images:
				for image in images:
					PostImage.objects.create(post=post_form, image=image)
			return redirect('home')
		return self.render_to_response({'post_form': post_form,})

	def test_func(self):
		if self.group:
			return self.request.user in self.group.members.all()
		return True

home_page_view = HomePageView.as_view()

class PostDetailView(LoginRequiredMixin, DetailView):
	model = Post

post_detail_view = PostDetailView.as_view()


class PostEditView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
	template_name = 'posts/post_edit.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		post = Post.objects.get(pk=kwargs['post_pk'])
		context['post'] = post
		context['form'] = PostEditForm(initial=model_to_dict(post))
		return context

	def post(self, request, *args, **kwargs):
		form = PostEditForm(request.POST)
		post = Post.objects.get(pk=kwargs['post_pk'])
		if form.is_valid():
			content = form.cleaned_data.get('content')
			post.content = content
			post.save()
		return redirect(request.POST.get('next'))

	def test_func(self):
		return self.request.user == Post.objects.get(pk=self.kwargs['post_pk']).user 

post_edit_view = PostEditView.as_view()

class DeletePostImageView(UserPassesTestMixin, LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		PostImage.objects.get(pk=kwargs['image_pk']).delete()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == PostImage.objects.get(pk=self.kwargs['image_pk']).post.user

delete_postimage_view = DeletePostImageView.as_view()

class AddPostImageView(UserPassesTestMixin, LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		images = request.FILES.getlist('images')
		post = Post.objects.get(pk=kwargs['post_pk'])
		if images:
			for image in images:
				PostImage.objects.create(post=post, image=image)
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == Post.objects.get(pk=self.kwargs['post_pk']).user

add_postimage_view = AddPostImageView.as_view()

class DeleteAllPostImageView(UserPassesTestMixin, LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		Post.objects.get(pk=kwargs['post_pk']).postimage_set.all().delete()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == Post.objects.get(pk=self.kwargs['post_pk']).user

delete_all_postimage_view = DeleteAllPostImageView.as_view()

class PostVideoView(UserPassesTestMixin, LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		post = Post.objects.get(pk=kwargs['post_pk'])
		post.video = None
		post.save()
		return redirect(request.META.get('HTTP_REFERER'))
	def post(self, request, *args, **kwargs):
		video = request.FILES.get('video')
		post = Post.objects.get(pk=kwargs['post_pk'])

		if video:
			post.video = video
			post.save()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == Post.objects.get(pk=self.kwargs['post_pk']).user

post_video_view = PostVideoView.as_view()

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		Post.objects.get(pk=kwargs['post_pk']).delete()
		return redirect('home')

	def test_func(self):
		post = Post.objects.get(pk=self.kwargs['post_pk'])
		if post.group:
			return self.request.user == post.user or self.request.user in post.group.members.all()
		return self.request.user == post.user

post_delete_view = PostDeleteView.as_view()

class PostLikesView(AjaxRequiredOnlyMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({'status': 'not logged in'})
		post = Post.objects.get(pk=kwargs['post_pk'])
		if request.user in post.likes.all():
			post.likes.remove(request.user)
			action = 'unlike'
		else:
			post.likes.add(request.user)
			action = 'like'
		return JsonResponse({'status': 'ok', 'action': action, 'num_of_likes': post.likes.all().count()})

post_likes_view = PostLikesView.as_view()

class CommentCreateView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		post = Post.objects.get(pk=kwargs['post_pk'])
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			form = comment_form.save(commit=False)
			form.user = request.user
			form.post = post
			form.save()
		return redirect(request.META.get('HTTP_REFERER'))

comment_create_view = CommentCreateView.as_view()

class ReplyCreateView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		comment = Comment.objects.get(pk=kwargs['comment_pk'])
		reply_form = ReplyForm(request.POST)
		if reply_form.is_valid():
			form = reply_form.save(commit=False)
			form.comment = comment
			form.user = request.user
			form.save()
		return redirect(request.META.get('HTTP_REFERER'))

reply_create_view = ReplyCreateView.as_view()

class CommentEditView(UserPassesTestMixin, LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		comment = Comment.objects.get(pk=kwargs['comment_pk'])
		comment_form = CommentForm(request.POST, instance=comment)
		if comment_form.is_valid():
			comment_form.save()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == Comment.objects.get(pk=self.kwargs['comment_pk']).user

comment_edit_view = CommentEditView.as_view()

class ReplyEditView(UserPassesTestMixin, LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		reply = Reply.objects.get(pk=kwargs['reply_pk'])
		reply_form = ReplyForm(request.POST, instance=reply)
		if reply_form.is_valid():
			reply_form.save()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == Reply.objects.get(pk=self.kwargs['reply_pk']).user

reply_edit_view = ReplyEditView.as_view()

class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		Comment.objects.get(pk=kwargs['comment_pk']).delete()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == Comment.objects.get(pk=self.kwargs['comment_pk']).user

comment_delete_view = CommentDeleteView.as_view()

class ReplyDeleteView(UserPassesTestMixin, LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		Reply.objects.get(pk=kwargs['reply_pk']).delete()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == Reply.objects.get(pk=self.kwargs['reply_pk']).user

reply_delete_view = ReplyDeleteView.as_view()

class CommentLikesView(AjaxRequiredOnlyMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({'status': 'not logged in'})
		comment = Comment.objects.get(pk=kwargs['comment_pk'])
		if request.user in comment.likes.all():
			comment.likes.remove(request.user)
			action = 'unlike'
		else:
			comment.likes.add(request.user)
			action = 'like'
		return JsonResponse({'status': 'ok', 'action': action, 'num_of_likes': comment.likes.all().count()})

comment_likes_view = CommentLikesView.as_view()

class ReplyLikesView(AjaxRequiredOnlyMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({'status': 'not logged in'})
		reply = Reply.objects.get(pk=kwargs['reply_pk'])
		if request.user in reply.likes.all():
			reply.likes.remove(request.user)
			action = 'unlike'
		else:
			reply.likes.add(request.user)
			action = 'like'
		return JsonResponse({'status': 'ok', 'action': action, 'num_of_likes': reply.likes.all().count()})

reply_likes_view = ReplyLikesView.as_view()

# class SharedPostCreateView(LoginRequiredMixin, View):
# 	def post(self, request, *args, **kwargs):
# 		print('post')
# 		post = Post.objects.get(pk=kwargs['post_pk'])
# 		shared_post_form = SharedPostForm(request.POST)
# 		print('Post:', request.POST)
# 		if shared_post_form.is_valid():
# 			form = shared_post_form.save(commit=False)
# 			form.post = post
# 			form.user = request.user
# 			form.save()
# 		return redirect('home')

# shared_post_create_view = SharedPostCreateView.as_view()



