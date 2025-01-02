from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:52929"  # Замените <MINIKUBE_SERVICE_URL> на URL вашего Minikube сервиса
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")