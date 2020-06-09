import json
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.edit import (
    CreateView, FormView, DeleteView, UpdateView)
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404

from .models import Link, Vote, Profile
from .forms import LinkForm, ProfileForm, VoteForm


# def link_list(request):
#     links = Link.with_votes.all()

#     template = 'links/list.html'
#     context = {'links': links}

#     return render(request, template, context)
class LinkListView(ListView):
    model = Link
    queryset = Link.with_votes.all()
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # qs: Links a user has voted for
            voted = Vote.objects.filter(voter=self.request.user)
            # qs: Links in a particular page
            links_in_page = [link.id for link in context["object_list"]]
            # list of links that have been voted
            voted = voted.filter(link_id__in=links_in_page)
            # Creates a list of link ids from the voted objects
            voted = voted.values_list('link_id', flat=True)
            context["voted"] = voted
        return context


class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    form_class = LinkForm

    def form_valid(self, form):
        f = form.save(commit=False)
        f.rank_score = 0.0
        f.submitter = self.request.user
        f.save()
        return super().form_valid(form)

# def link_create(request):
#     if request.method == 'POST':
#         form = LinkForm(request.POST)
#         if form.is_valid():
#             f = form.save(commit=False)
#             f.rank_score = 0.0
#             f.submitter = request.user
#             f.save()
#             redirect('/')
#     else:
#         form = LinkForm()

#     template = 'links/form.html'
#     context = {'form': form}

#     return render(request, template, context)


class LinkDetailView(DetailView):
    model = Link

# def link_detail(request, pk):
#     link = get_object_or_404(Link, pk=pk)

#     template = 'links/detail.html'
#     context = {'link': link}

#     return render(request, template, context)


class LinkUpdateView(LoginRequiredMixin, UpdateView):
    model = Link
    form_class = LinkForm

# def link_update(request, pk):
#     link = get_object_or_404(Link, pk=pk)

#     if request.method == 'POST':
#         form = LinkForm(request.POST, instance=link)
#         if form.is_valid():
#             form.save()
#             redirect('/')
#     else:
#         form = LinkForm(instance=link)

#     template = 'links/form.html'
#     context = {'link': link, 'form': form}

#     return render(request, template, context)


class LinkDeleteView(LoginRequiredMixin, DeleteView):
    model = Link
    success_url = reverse_lazy("home")


class ProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        Profile.objects.get_or_create(user=user)
        return user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "edit_profile.html"

    def get_object(self, queryset=None):
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("profile", kwargs={"slug": self.request.user})

# def profile(request, username):
#     user = get_object_or_404(Profile, user=username)

#     template = 'links/user_detail.html'
#     context = {'user': user}

#     return render(request, template, context)


def settings(request, username):
    user = get_object_or_404(Profile, user=request.username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            return reverse("profile", kwargs={'slug': request.user})
    else:
        form = ProfileForm(instance=request.user)

    template = 'links/user_settings.html'
    context = {'user': user, 'form': form}

    return render(request, template, context)


# def vote(request):
#     link = get_object_or_404(Link, pk=form.data['link'])
#     user = request.user
#     previous_votes = Vote.objects.filter(voter=user, link=link)
#     has_voted = (previous_votes.count() > 0)
#     form = VoteForm()
#     if not has_voted:
#         Vote.objects.create(voter=user, link=link)
#         print("voted")
#     else:
#         previous_votes[0].delete()
#         print("unvoted")
#     return redirect('link_list')

class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(
            vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response


class VoteFormBaseView(LoginRequiredMixin, FormView):
    form_class = VoteForm

    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        link = get_object_or_404(Link, pk=form.data['link'])
        user = self.request.user
        previous_vote = Vote.objects.filter(voter=user, link=link)
        has_voted = (len(previous_vote) > 0)
        ret = {"success": 1}
        if not has_voted:
            v = Vote.objects.create(voter=user, link=link)
            ret["voteobj"] = v.id
        else:
            previous_vote[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret, True)

    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors}
        return self.create_response(ret, False)


class VoteFormView(JSONFormMixin, VoteFormBaseView):
    pass
