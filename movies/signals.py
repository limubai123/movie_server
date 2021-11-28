from django.db.models.signals import pre_save
from django.dispatch import receiver

from movies.models import Vote


@receiver(pre_save, sender=Vote)
def update_voting_count(sender, instance, **kwargs):
    movie_object = instance.movie
    older_vote = Vote.objects.filter(user=instance.user, movie=instance.movie).first()
    if older_vote:
        if older_vote.vote_nature != instance.vote_nature:
            if instance.vote_nature == Vote.UP:
                movie_object.upvote_count += 1
                movie_object.downvote_count -= 1
            else:
                movie_object.downvote_count += 1
                movie_object.upvote_count -= 1
        else:
            return
    else:
        if instance.vote_nature == Vote.UP:
            movie_object.upvote_count += 1
        else:
            movie_object.downvote_count += 1
    movie_object.save()
