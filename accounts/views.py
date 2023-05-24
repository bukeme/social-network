from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from allauth.account.views import SignupView
from allauth.account.forms import ChangePasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import (
	UserSignUpForm,
	UserProfileForm,
	UserForm,
	UserProfileSettingsForm,
	UserProfileImageForm,
	UserCoverImageForm
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms.models import model_to_dict
from posts.models import Post, PostImage
from accounts.utils import get_all_photos, get_friend_request_object
from posts.decorators import AjaxRequiredOnlyMixin
from accounts.models import UserProfile, FriendRequest

# Create your views here.

class UserSignUpView(SignupView):
	form_class = UserSignUpForm

user_signup_view = UserSignUpView.as_view()

class ProfilePostView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/profile_post.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		user = get_object_or_404(User, pk=kwargs['user_pk'])
		context['posts'] = Post.objects.filter(user=user)
		context['recent_photos'] = get_all_photos(self.request, user.pk)[:6]
		context['user'] = user
		context['page'] = 'profile_post'
		context['userprofile_form'] = UserProfileForm(initial=model_to_dict(user.userprofile))
		context['user_form'] = UserForm(initial=model_to_dict(user))
		return context

profile_post_view = ProfilePostView.as_view()

class ProfileAboutView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/profile_about.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		user = get_object_or_404(User, pk=kwargs['user_pk'])
		context['user'] = user
		context['page'] = 'profile_about'
		context['userprofile_form'] = UserProfileForm(initial=model_to_dict(user.userprofile))
		context['user_form'] = UserForm(initial=model_to_dict(user))
		# print(user.userprofile._meta.get_fields())
		field_dict = {}
		icon_classes = {'marital_status': 'fa fa-heart', 'birth_date': 'fa fa-calendar', 'occupation': 'fa fa-briefcase', 'location': 'fa fa-map-marker-alt', 'date_joined': 'fa fa-calendar', 'email': 'fa fa-envelope'}
		field_notes = {'marital_status': 'Status', 'birth_date': 'Born', 'occupation': '', 'location': 'Lives in', 'date_joined': 'Joined on', 'email': 'Email'}
		for field in user.userprofile._meta.fields:
			if field.name in ('marital_status', 'birth_date', 'occupation', 'location'):
				field_dict[field.name] = {
					'icon_class': icon_classes[field.name],
					'field_note': field_notes[field.name],
					'field_value': getattr(user.userprofile, field.name),
					'model_name': 'userprofile',
				}
		for field in user._meta.fields:
			if field.name in ('date_joined', 'email',):
				field_dict[field.name] = {
					'icon_class': icon_classes[field.name],
					'field_note': field_notes[field.name],
					'field_value': getattr(user, field.name),
					'model_name': 'user',
				}
		context['field_dict'] = field_dict
		return context

profile_about_view = ProfileAboutView.as_view()

class ProfilePhotosView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/profile_photos.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user = User.objects.get(pk=kwargs['user_pk'])
		context['user'] = user
		context['post_photos'] = PostImage.objects.filter(
			post__user=user
		).filter(
			Q(post__visibility='public') | Q(post__user=self.request.user)
		)
		context['page'] = 'profile_photos'
		return context

profile_photos_view = ProfilePhotosView.as_view()

class UpdateUserProfileDataView(UserPassesTestMixin, LoginRequiredMixin, View):
	user = None

	def dispatch(self, request, *args, **kwargs):
		self.user = get_object_or_404(User, pk=kwargs['user_pk'])
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form = UserProfileForm(
			request.POST,
			instance=self.user.userprofile
		)
		if form.is_valid():
			form.save()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == self.user 

update_user_profile_data_view = UpdateUserProfileDataView.as_view()

class UpdateUserDataView(UserPassesTestMixin, LoginRequiredMixin, View):
	user = None

	def dispatch(self, request, *args, **kwargs):
		self.user = get_object_or_404(User, pk=kwargs['user_pk'])
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		form = UserForm(
			request.POST,
			instance=self.user,
		)
		if form.is_valid():
			form.save()
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		return self.request.user == self.user 

update_user_data_view = UpdateUserDataView.as_view()

class UserSettingsView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/settings.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['profile_form'] = UserProfileSettingsForm(initial=model_to_dict(self.request.user.userprofile))
		context['user_form'] = UserForm(initial=model_to_dict(self.request.user))
		context['password_form'] = PasswordChangeForm(self.request.user)
		return context

	def post(self, request, *args, **kwargs):
		data = request.POST
		user_form = UserForm(data, instance=request.user)
		profile_form = UserProfileSettingsForm(data, instance=request.user.userprofile) 
		password_form = PasswordChangeForm(request.user, data)
		if 'user-profile-form' in data:
			if user_form.is_valid() and profile_form.is_valid():
				user_form.save()
				profile_form.save()
				messages.success(request, 'Profile updated successfully')
				return redirect('user_settings')
		elif 'password-form' in data:
			if password_form.is_valid():
				user = password_form.save()
				update_session_auth_hash(request, user)
				messages.success(request, 'Your password was changed successfully')
				return redirect('user_settings')
			else:
				messages.error(request, 'An error occured from your input')
		return self.render_to_response({'user_form': user_form, 'profile_form': profile_form, 'password_form': password_form,})

user_settings_view = UserSettingsView.as_view()

class UpdateUserProfileView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
	template_name = 'accounts/profile-edit.html'

	def post(self, request, *args, **kwargs):
		user = User.objects.get(pk=kwargs['user_pk'])
		user_form = UserForm(request.POST, instance=user)
		profile_form = UserProfileForm(request.POST, instance=user.userprofile)
		profile_image_form = UserProfileImageForm(request.POST, request.FILES)
		cover_image_form = UserCoverImageForm(request.POST, request.FILES)

		if user_form.is_valid() and profile_form.is_valid() and profile_image_form.is_valid() and cover_image_form.is_valid():
			user_form.save()
			user_profile = profile_form.save()
			if request.FILES.get('profile_image'):
				profile_image = profile_image_form.save(commit=False)
				profile_image.userprofile = user_profile
				profile_image.save()
			if request.FILES.get('cover_image'):
				cover_image = cover_image_form.save(commit=False)
				cover_image.userprofile = user_profile
				cover_image.save()
			messages.success(request, 'Your Profile Has Been Updated Successfully')
			return redirect(request.META.get('HTTP_REFERER'))
		return self.render_to_response({
			'user_form': user_form,
			'profile_form': profile_form,
			'profile_image_form': profile_image_form,
			'cover_image_form': cover_image_form,
		})

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user = User.objects.get(pk=kwargs['user_pk'])
		context['user'] = user
		context['user_form'] = UserForm(initial=model_to_dict(user))
		context['profile_form'] = UserProfileForm(initial=model_to_dict(user.userprofile))
		context['profile_image_form'] = UserProfileImageForm()
		context['cover_image_form'] = UserCoverImageForm()
		return context 

	def test_func(self):
		return self.request.user == User.objects.get(pk=self.kwargs['user_pk'])

update_user_profile_view = UpdateUserProfileView.as_view()

class FollowView(AjaxRequiredOnlyMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({'status': 'not logged in'})
		userprofile = User.objects.get(pk=kwargs['user_pk']).userprofile
		if request.user in userprofile.followers.all():
			userprofile.followers.remove(request.user)
			action = 'unfollow'
		else:
			userprofile.followers.add(request.user)
			action = 'follow'

		return JsonResponse(
			{
				'status': 'ok',
				'action': action,
				'num_of_followers': userprofile.followers.all().count(),
			}
		)

follow_view = FollowView.as_view()

# class FollowersListView(LoginRequiredMixin, TemplateView):
# 	template_name = 'accounts/user_followers_list.html'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super().get_context_data(*args, **kwargs)
# 		context['user'] = User.objects.get(pk=kwargs['user_pk'])
# 		context['page'] = 'followers'
# 		print(self.request.user.followed_users.all())
# 		return context

# followers_list_view = FollowersListView.as_view()

# class FollowingListView(LoginRequiredMixin, TemplateView):
# 	template_name = 'accounts/user_following_list.html'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super().get_context_data(*args, **kwargs)
# 		context['user'] = User.objects.get(pk=kwargs['user_pk'])
# 		context['page'] = 'following'
# 		# context['followed_users'] = UserProfile.objects.filter(followers__in=)


class FollowListView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(pk=kwargs['user_pk'])
		if kwargs['follow_type'] == 'followers':
			template_name = 'accounts/user_followers_list.html'
			page = 'followers'
		elif kwargs['follow_type'] == 'following':
			template_name = 'accounts/user_following_list.html'
			page = 'following'
		context = {'user': user, 'page': page,}
		return render(request, template_name, context)

follow_list_view = FollowListView.as_view()

class SendFriendRequestView(LoginRequiredMixin, UserPassesTestMixin, View):
	def post(self, request, *args, **kwargs):
		to_user = User.objects.get(pk=kwargs['to_user_pk'])
		obj, created = FriendRequest.objects.get_or_create(
			from_user=request.user, to_user=to_user
		)
		if not created:
			messages.warning(request, 'Friend Request Already Sent')
		
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		to_user = User.objects.get(pk=self.kwargs['to_user_pk'])
		return self.request.user != to_user and to_user not in self.request.user.userprofile.friends.all()

send_friend_request_view = SendFriendRequestView.as_view()

class DeleteFriendRequestView(LoginRequiredMixin, UserPassesTestMixin, View):
	def post(self, request, *args, **kwargs):
		get_friend_request_object(
			to_user_pk=kwargs['to_user_pk'], from_user_pk=kwargs['from_user_pk']
		).delete()
		messages.error(request, 'Friend Request Deleted')
		return redirect(request.META.get('HTTP_REFERER'))

	def test_func(self):
		friend_request = get_friend_request_object(
			to_user_pk=self.kwargs['to_user_pk'], from_user_pk=self.kwargs['from_user_pk']
		)
		return self.request.user == friend_request.from_user or self.request.user == friend_request.to_user

delete_friend_request_view = DeleteFriendRequestView.as_view()

class AcceptFriendRequestView(LoginRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		friend_request = get_friend_request_object(
			to_user_pk=request.user.pk, from_user_pk=kwargs['from_user_pk']
		)
		to_user, from_user = friend_request.to_user, friend_request.from_user
		to_user.userprofile.friends.add(from_user)
		from_user.userprofile.friends.add(to_user)
		friend_request.delete()
		return redirect(request.META.get('HTTP_REFERER'))

accept_friend_request_view = AcceptFriendRequestView.as_view()

class FriendRequestListView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/friend_request_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		fr_users = FriendRequest.objects.filter(
			to_user=self.request.user
		).values_list('from_user', flat=True)
		context['friend_request_from_users'] = [User.objects.get(pk=pk) for pk in fr_users]
		context['page'] = 'friend_request_list'
		return context

friend_request_list_view = FriendRequestListView.as_view()

class FriendListView(LoginRequiredMixin, TemplateView):
	template_name = 'accounts/friend_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user = User.objects.get(pk=kwargs['user_pk'])
		search_friend = self.request.GET.get('search_friend', '')
		context['friends'] = user.userprofile.friends.all().filter(
			Q(first_name__icontains=search_friend) |
			Q(last_name__icontains=search_friend) |
			Q(username__icontains=search_friend)
		)
		context['user'] = user
		context['page'] = 'profile_friends'
		return context

friend_list_view = FriendListView.as_view()

class RemoveFriendView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		friend = User.objects.get(pk=kwargs['user_pk'])
		friend_name = friend.userprofile.full_name
		request.user.userprofile.friends.remove(friend)
		messages.error(request, f'You have removed {friend_name} as your friend')
		return redirect(request.META.get('HTTP_REFERER'))

remove_friend_view = RemoveFriendView.as_view()

