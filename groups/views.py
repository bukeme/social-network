from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from groups.models import CustomGroup
from groups.forms import GroupCreateForm, GroupProfileImageForm
from groups.utils import get_all_group_photos, get_all_group_videos
from accounts.utils import filter_user_queryset

# Create your views here.

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = CustomGroup
    form_class = GroupCreateForm
    template_name = 'groups/group_create.html'

    def form_valid(self, form):
        form = form.save()
        form.owner = self.request.user
        form.members.add(self.request.user)
        form.admin_members.add(self.request.user)
        form.save()
        return redirect(form.get_absolute_url())

group_create_view = GroupCreateView.as_view()

class GroupListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        filter_str = self.kwargs.get('group')
        url_path = self.request.path
        query = self.request.GET.get('query', '')
        print(query)
        if filter_str == 'my-groups':
            if 'search' in url_path:
                queryset = self.request.user.group.all().filter(name__icontains=query)
            else:
                queryset = self.request.user.group.all()
        elif filter_str == 'all-groups':
            if 'search' in url_path:
                queryset = CustomGroup.objects.all().filter(name__icontains=query)
            else:
                queryset = CustomGroup.objects.all()
        print(self.request.path)
        return queryset

group_list_view = GroupListView.as_view()

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = CustomGroup
    context_object_name = 'group'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['posts'] = self.object.post_set.all().order_by('-created')
        return context
    
group_detail_view = GroupDetailView.as_view()

group_about_view = GroupDetailView.as_view(template_name = 'groups/group_about.html')

class GroupMembersListView(LoginRequiredMixin, DetailView):
    model = CustomGroup
    context_object_name = 'group'
    template_name = 'groups/group_members.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get('search_member')
        if query:
            group_members = filter_user_queryset(self.object.members.all(), query)
        else:
            group_members = self.object.members.all().difference(
                self.object.admin_members.all(),
            )
        context['group_members'] = group_members
        return context 

group_members_list_view = GroupMembersListView.as_view()

class JoinGroupView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group = CustomGroup.objects.get(pk=kwargs['group_pk'])
        user = User.objects.get(pk=kwargs['user_pk'])
        if user in group.members.all():
            group.members.remove(user)
            group.admin_members.remove(user)
        else:
            group.members.add(user)
        group.save()
        return redirect(request.META.get('HTTP_REFERER'))

join_group_view = JoinGroupView.as_view()

class GroupPhotosView(LoginRequiredMixin, TemplateView):
    template_name = 'groups/group_photos.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['photos'] = get_all_group_photos(kwargs['group_pk'])
        context['group'] = CustomGroup.objects.get(pk=kwargs['group_pk'])
        return context 

group_photos_view = GroupPhotosView.as_view()

class GroupVideosView(LoginRequiredMixin, TemplateView):
    template_name = 'groups/group_videos.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['videos'] = get_all_group_videos(kwargs['group_pk'])
        context['group'] = CustomGroup.objects.get(pk=kwargs['group_pk'])
        return context

group_videos_view = GroupVideosView.as_view()

class GroupSettingsView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = 'groups/group_settings.html'

    def dispatch(self, request, *args, **kwargs):
        self.group = CustomGroup.objects.get(pk=kwargs['group_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['group'] = self.group
        context['image_form'] = GroupProfileImageForm()
        context['group_form'] = GroupCreateForm(instance=self.group)
        return context

    def post(self, request, *args, **kwargs):
        image_form = GroupProfileImageForm(request.POST, request.FILES)
        group_form = GroupCreateForm(request.POST, instance=self.group)

        if image_form.is_valid() and group_form.is_valid():
            group_form.save()
            if request.FILES.get('image'):
                image_form = image_form.save(commit=False)
                image_form.group = self.group
                image_form.save()
            messages.success(request, 'Group Update Was Successful')
            return redirect(request.META.get('HTTP_REFERER'))
        return self.render_to_response({'image_form': image_form, 'group_form': group_form})

    def test_func(self):
        return self.request.user in self.group.admin_members.all()

group_settings_view = GroupSettingsView.as_view()

class GroupSearchView(LoginRequiredMixin, ListView):
    template_name = 'groups/group_search.html'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        queryset = CustomGroup.objects.filter(name__icontains=query)
        return queryset

group_search_view = GroupSearchView.as_view()

