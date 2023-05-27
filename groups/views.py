from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from groups.models import CustomGroup
from groups.forms import GroupCreateForm

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
        context['posts'] = self.object.post_set.all()
        return context
    
group_detail_view = GroupDetailView.as_view()

group_about_view = GroupDetailView.as_view(template_name = 'groups/group_about.html')

class GroupMembersListView(LoginRequiredMixin, DetailView):
    model = CustomGroup
    context_object_name = 'group'
    template_name = 'groups/group_members.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['group_members'] = self.object.members.all().difference(self.object.admin_members.all(), User.objects.filter(pk=self.request.user.pk))
        return context 

group_members_list_view = GroupMembersListView.as_view()

class JoinGroupView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        group = CustomGroup.objects.get(pk=kwargs['group_pk'])
        if request.user in group.members.all():
            group.members.remove(request.user)
        else:
            group.members.add(request.user)
        group.save()
        return redirect(request.META.get('HTTP_REFERER'))

join_group_view = JoinGroupView.as_view()
