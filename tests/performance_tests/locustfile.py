from locust import HttpUser, task

class ProjectPerfTest(HttpUser):

    @task
    def update_and_check(self):
        """ Instructions that connect, book a place for an event and check the detailed board """
        
        self.client.post('/showSummary', {'email':'admin@irontemple.com'})
        self.client.post('/purchasePlaces', {'competition': 'Fall Classic',
                                             'club': 'Iron Temple',
                                             'places': 1,
                                             'time': '2022-10-22 13:30:00'
                                             })
        self.client.get('/detailed-board')
