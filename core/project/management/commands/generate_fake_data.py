from django.core.management.base import BaseCommand
from faker import Faker
from random import randint
from project.models import Apps

some_docker_images = [
    'nginx',
    'busybox',
    'redis',
]

class Command(BaseCommand):
    help = 'creating 10 different random apps for better test experience'

    def __init__(self, *args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)
        self.faker = Faker()

    def handle(self, *args, **options):
        # creating 10 apps
        for i in range(10):
            app = Apps.objects.create(
                name = f"App number {i+1}",
                image = some_docker_images[randint(0, len(some_docker_images)-1)],
                envs = [
                        f"key{i}=val{i}",
                        f"key{i+1}=val{i+1}"
                    ],
                command = f'sleep 100{i+1}'
            )
            print(f"{app} CREATED!")