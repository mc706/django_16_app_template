import json
from urllib import urlencode
from django.core.management import call_command
from django.test import TestCase
from django.test.client import Client


class ObjectAPITest(TestCase):
    fixtures = ['initial_data.json', 'test_user_data.json']

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.username = 'user'
        self.password = 'password'
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
        #call_command('loaddata', 'test_data.json', verbosity=1)

    def test_list_objects(self):
        #Test success
        response = self.client.get('/api/objects/')
        self.assertEqual(response.status_code, 200,
                         "GET didn't respond 200. Instead responded %s" % response.status_code)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2, "2 Objects From Fixture Not Returned. Instead %s found." % len(data))
        #test reject not get methods
        response = self.client.post('/api/objects/', {'test': 'data'})
        self.assertEqual(response.status_code, 405,
                         "POST method not rejected. Instead responded %s" % response.status_code)

    def test_create_object(self):
        response = self.client.post('/api/objects/new/', {
            "name": "Testy Object",
        })
        self.assertEqual(response.status_code, 201,
                         "POST didnt return 201. Instead responded %s" % response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'Testy Object', "Data didn't return same as it was sent")
        self.assertEqual(data['slug'], 'testy-object', "Object didn't get assigned a slug")

    def test_get_object(self):
        response = self.client.get('/api/objects/test-object/')
        self.assertEqual(response.status_code, 200,
                         "GET didnt return 200.. Instead responded %s" % response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['title'], "Test Object", "Title mismatch")
        #test invalid object name returns 404
        response = self.client.get('/api/objects/not-a-object/')
        self.assertEqual(response.status_code, 404,
                         "Invalid GET didn't return 404. Instead responded %s" % response.status_code)

    def test_update_object(self):
        response = self.client.put(
            '/api/objects/test-object/',
            data=urlencode({
                "name": "Test Object"
            }),
            content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 200,
                         "PUT did  not respond 200. Instead responded %s" % response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['abbreviation'], "TSTY", "abbreviation didn't update")
        #test invalid object name returns 404
        response = self.client.put(
            '/api/objects/not-a-object/',
            data=urlencode({
                "name": "Test Object"
            }),
            content_type='application/x-www-form-urlencoded')
        self.assertEqual(response.status_code, 404,
                         "Invalid PUT didn't respond 404. Instead responded %s" % response.status_code)

    def test_delete_object(self):
        response = self.client.delete('/api/objects/other-object/')
        self.assertEqual(response.status_code, 200,
                         "Delete didn't respond 200. Instead responded %s" % response.status_code)
        #test invalid object name returns 404
        response = self.client.delete('/api/objects/not-a-object/')
        self.assertEqual(response.status_code, 404,
                         "Invalid Delete didn't respond 404. Instead responded %s" % response.status_code)