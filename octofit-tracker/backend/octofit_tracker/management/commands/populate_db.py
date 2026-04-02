from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import models as octo_models

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        # Delete in child-to-parent order to avoid Djongo issues
        for model in [octo_models.Activity, octo_models.Leaderboard, octo_models.Workout, get_user_model(), octo_models.Team]:
            for obj in model.objects.all():
                if getattr(obj, 'pk', None):
                    obj.delete()

        # Create teams
        marvel = octo_models.Team.objects.create(name='Marvel')
        dc = octo_models.Team.objects.create(name='DC')

        # Create users
        ironman = get_user_model().objects.create_user(username='ironman', email='ironman@marvel.com', password='password', team=marvel)
        captain = get_user_model().objects.create_user(username='captain', email='captain@marvel.com', password='password', team=marvel)
        batman = get_user_model().objects.create_user(username='batman', email='batman@dc.com', password='password', team=dc)
        superman = get_user_model().objects.create_user(username='superman', email='superman@dc.com', password='password', team=dc)

        # Create activities
        octo_models.Activity.objects.create(user=ironman, type='run', duration=30, distance=5)
        octo_models.Activity.objects.create(user=batman, type='cycle', duration=60, distance=20)

        # Create workouts
        octo_models.Workout.objects.create(name='Morning Cardio', description='Cardio for all heroes')
        octo_models.Workout.objects.create(name='Strength Training', description='Strength for all heroes')

        # Create leaderboard
        octo_models.Leaderboard.objects.create(user=ironman, points=100)
        octo_models.Leaderboard.objects.create(user=batman, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
