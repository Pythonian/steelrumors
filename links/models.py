from django.conf import settings
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL


class LinkVoteCountManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .annotate(votes=Count('vote'))\
            .order_by('-rank_score', '-votes')


class Link(models.Model):
    title = models.CharField("Headline", max_length=100)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_on = models.DateTimeField(auto_now_add=True)
    rank_score = models.FloatField(default=0.0)
    url = models.URLField("URL", max_length=250, blank=True)
    description = models.TextField(blank=True)

    objects = models.Manager()
    with_votes = LinkVoteCountManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('link_detail', kwargs={'pk': self.id})

    def set_rank(self):
        """ Ranks how a link is displayed """
        SECS_IN_HOUR = float(60 * 60)
        GRAVITY = 1.2

        # difference btw current time and time link was submitted
        delta = now() - self.submitted_on
        # Convert delta into no. of hours
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age + 2), GRAVITY)
        # saves to database
        self.save()


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.voter.username} voted {self.link.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True)

    def __str__(self):
        return f'{self.user.username}'


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(create_profile, sender=User)
