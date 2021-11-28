from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from movies.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        # user = User.objects.create(username="admin")
        # user.set_password("12345")
        # user.save()
        print("======user created=========")

        Genre.objects.create(name="Comedy")
        Genre.objects.create(name="Action")
        Genre.objects.create(name="Drama")
        Genre.objects.create(name="Romance")
        Genre.objects.create(name="War")
        Genre.objects.create(name="Mistery")
        Genre.objects.create(name="Crime")
        print("======genres created=========")
