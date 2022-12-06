from django.urls import reverse
from django.test import TestCase, Client
from random import randint
from project.management.commands.generate_fake_data import some_docker_images
from .models import Apps

class TestBlogView(TestCase):
    def setUp(self):
        self.client = Client()
        for i in range(5):
            Apps.objects.create(
                name = f"App number {i+1}",
                image = some_docker_images[randint(0, len(some_docker_images)-1)],
                envs = [
                        f"key{i}=val{i}",
                        f"key{i+1}=val{i+1}"
                    ],
                command = f'sleep 100{i+1}'
            )

    def test_create_new_apps(self):
        url = reverse('api-v1:manage-apps-list')
        response = self.client.post(url, data={
            "name": f"test-app",
            "image": f"test-image",
            "envs": '["key1=val1", "key2=val2"]',
            "command": "sleep 1000"
        }, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(str(response.content).find('test-app'))

    def test_list_of_apps(self):
        url = reverse('api-v1:manage-apps-list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        for i in range(1, 6):
            self.assertTrue(str(response.content).find(f'App number {i}'))

    def test_retrieve_single_app_detail(self):
        for i in range(1, 6):
            url = reverse('api-v1:manage-apps-detail', kwargs={'pk':f"{i}"})
            response = self.client.get(url)
            self.assertEquals(response.status_code, 200)
            self.assertTrue(str(response.content).find(f'App number {i}'))
    
    def test_update_single_app(self):
        url = reverse('api-v1:manage-apps-detail', kwargs={'pk':"1"})
        response = self.client.put(url, data={
            "name": "updated-test-app",
            "image": "updated-test-image",
            "envs": '["key1=updated-val1", "key2=updated-val2"]',
            "command": "updated sleep 1000"
        }, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertTrue(str(response.content).find("updated-test-app"))
        
    def test_delete_single_app(self):
        url = reverse('api-v1:manage-apps-detail', kwargs={'pk':"5"})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, 204)

    def test_run_container(self):
        # create container from app
        url = reverse('api-v1:run-container', kwargs={'pk':"1"})
        response_run_container = self.client.get(url)
        self.assertEquals(response_run_container.status_code, 200)
        test_container_id = response_run_container.data["id"]

        # check if container is available in monitoring
        url = reverse('api-v1:container-monitoring')
        response_monitoring = self.client.get(url)
        self.assertEquals(response_monitoring.status_code, 200)
        self.assertTrue(str(response_monitoring.content).find(test_container_id))
        