from django import forms
from .models import Link, Profile, Vote


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ['submitter', 'rank_score']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'
