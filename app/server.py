from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return f"Hello this srinivas allibilli Successfully implemented the project by setting up a CI/CD pipeline, containerizing the application using Docker, deploying it on AWS (ECS/Fargate), and automating infrastructure with Terraform — achieving faster release cycles and improved reliability.”from ECS Fargate! Environment: {os.getenv('ENV', 'DEV','TEST')}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
