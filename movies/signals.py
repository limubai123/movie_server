from django.db.models.signals import pre_save
from django.dispatch import receiver

from movies.models import Vote


@receiver(pre_save, sender=Vote)
def update_voting_count(sender, instance, created, **kwargs):
    movie_object = instance.movie
    if created:
        if instance.vote_nature == Vote.UP:
            movie_object.upvote_count += 1
        else:
            movie_object.downvote_count += 1
    else:
        older_vote = Vote.objects.get(pk=instance.pk)
        if older_vote.vote_nature != instance.vote_nature:
            if instance.vote_nature == Vote.UP:
                movie_object.upvote_count += 1
                movie_object.downvote_count -= 1
            else:
                movie_object.downvote_count += 1
                movie_object.upvote_count -= 1
        else:
            return
    movie_object.save()
