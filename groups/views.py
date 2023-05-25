from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import TemplateView, CreateView, ListView
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
        if filter_str == 'my-groups':
            queryset = self.request.user.group.all()
        elif filter_str == 'all-groups':
            queryset = CustomGroup.objects.all()
        return queryset

group_list_view = GroupListView.as_view()
