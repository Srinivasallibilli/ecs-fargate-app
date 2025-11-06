from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return f"Hello Successfully implemented the project by setting up a CI/CD pipeline, containerizing the application using Docker, deploying it on AWS (ECS/Fargate) from ECS Fargate! Environment: {os.getenv('ENV', 'dev')}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
