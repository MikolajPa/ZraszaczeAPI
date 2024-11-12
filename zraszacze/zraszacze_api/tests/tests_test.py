from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from zraszacze.zraszacze_api.models import Todo

class TodoApiTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_todo_list_api_view(self):
        # Create some sample Todos
        Todo.objects.create(title='Task 1', description='Description 1')
        Todo.objects.create(title='Task 2', description='Description 2')

        # Get the API URL using reverse
        url = reverse('todo-list')

        # Make a GET request to the API endpoint
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the response is in JSON format
        response_data = response.json()

        # Check if the response contains the expected data
        todos = Todo.objects.all()
        self.assertEqual(len(response_data), todos.count())

        # Check if each todo item is in the response
        for todo in todos:
            todo_in_response = next((item for item in response_data if item['title'] == todo.title), None)
            self.assertIsNotNone(todo_in_response)
            self.assertEqual(todo_in_response['description'], todo.description)

    # Additional test cases for other views
