# 🚀 Deploy Dockerized App on AWS ECS Fargate with CI/CD

This project demonstrates **deploying a Dockerized Python Flask app** to **AWS ECS Fargate** using **CodePipeline and CodeBuild** for a fully automated CI/CD workflow.  
The app runs serverlessly on Fargate and is exposed publicly through an **Application Load Balancer (ALB)**.

---

## 🗂️ Table of Contents

1. [Project Overview](#project-overview)  
2. [Architecture Diagram](#architecture-diagram)  
3. [Project Structure](#project-structure)  
4. [Prerequisites](#prerequisites)  
5. [Step-by-Step Implementation](#step-by-step-implementation)  
   - [Step 1: Dockerize the App](#step-1-dockerize-the-app)  
   - [Step 2: Push to Amazon ECR](#step-2-push-to-amazon-ecr)  
   - [Step 3: ECS Task Definition](#step-3-ecs-task-definition)  
   - [Step 4: Application Load Balancer (ALB)](#step-4-application-load-balancer-alb)  
   - [Step 5: ECS Service Setup](#step-5-ecs-service-setup)  
   - [Step 6: CI/CD Pipeline](#step-6-cicd-pipeline)  
   - [Step 7: Verification & Scaling](#step-7-verification--scaling)  
6. [Key Takeaways](#key-takeaways)  
7. [Enhancements](#enhancements)  
8. [Author](#author)

---

## 📘 Project Overview

**Goal:**  
Build, containerize, and deploy a Flask-based web application using AWS Fargate — without managing servers.  
Integrate a CI/CD pipeline to automate build, test, and deploy processes.

**Services Used:**  
- **Amazon ECR** – Container registry  
- **Amazon ECS (Fargate)** – Serverless container compute  
- **Application Load Balancer (ALB)** – HTTP routing  
- **CodePipeline** – Continuous integration and delivery  
- **CodeBuild** – Automated build and Docker push  
- **CloudWatch** – Monitoring and logging  

---

## 🏗️ Architecture Diagram

![Architecture Diagram](https://via.placeholder.com/1000x500.png?text=ECS+Fargate+CI/CD+Architecture)

**Workflow:**

GitHub → CodePipeline → CodeBuild → ECR → ECS Fargate → ALB → User
Project Structure
ecs-fargate-app/
├── app/ # Python Flask application
├── Dockerfile # Docker build configuration
├── requirements.txt # Python dependencies
├── buildspec.yml # Build instructions for CodeBuild
├── ecs-task-def.json # ECS Task Definition for container setup
├── pipeline.yml # Optional: CI/CD IaC
└── README.md # Project documentation

---

## ⚙️ Prerequisites

Before you start:

✅ AWS account with permissions for ECS, ECR, ALB, CodePipeline, and CodeBuild  
✅ AWS CLI installed & configured (`aws configure`)  
✅ Docker installed locally  
✅ GitHub repository (linked with CodePipeline)  

---

## 🪄 Step-by-Step Implementation

---

### 🧱 Step 1: Dockerize the App

1. Create your Flask app inside the `app/` directory.  
2. Make sure your Flask app listens on **port 5000** (`app.run(host="0.0.0.0", port=5000)`).
3. Create a Dockerfile that installs dependencies and runs your app.

Test locally:
```bash
docker build -t ecs-fargate-app .
docker run -p 5000:5000 ecs-fargate-app
Visit: http://localhost:5000
Step 2: Push to Amazon ECR

1.Create a repository:
aws ecr create-repository --repository-name ecr-fargate-app --region <your-region>
2.Authenticate Docker with ECR:
aws ecr get-login-password --region <region> \
| docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
3.Build and push your image:
docker build -t ecr-fargate-app .
docker tag ecr-fargate-app:latest <account-id>.dkr.ecr.<region>.amazonaws.com/ecr-fargate-app:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ecr-fargate-app:latest
🧩 Step 3: ECS Task Definition
.Create a JSON file (ecs-task-def.json) defining:
.Container image from ECR
.Port mappings (5000 → 5000)
.CPU & memory limits
.Log configuration

Register it:
aws ecs register-task-definition --cli-input-json file://ecs-task-def.json
🌐 Step 4: Application Load Balancer (ALB)
1.Create ALB in public subnets.
2.Create Target Group (type: IP, port 5000).
3.Set Health Check Path: /
4.Configure Security Groups:
 .ALB: allow inbound HTTP (port 80)
 .ECS: allow inbound only from ALB SG
🧭 Step 5: ECS Service Setup
.Launch ECS service using Fargate.
.Link Task Definition + Target Group.
.Choose desired count (1 or more).
.Enable Auto-assign public IP.
Check if ECS task is Healthy in Target Group.
🔄 Step 6: CI/CD Pipeline
.CodePipeline Flow:
GitHub (Source)
   ↓
CodeBuild (Build & Push to ECR)
   ↓
ECS Deploy (Update running service)

.Create CodeBuild project with:

  .Environment: Linux / Standard Image
  .Privileged mode: Enabled
  .buildspec.yml file reference
.Create CodePipeline linked to GitHub repository.
.Add stages: Source → Build → Deploy.

Pipeline Output:
✅ Automatically builds & deploys new versions on every Git commit.

✅ Step 7: Verification & Scaling
1.Visit the ALB DNS name in your browser:
    http://<your-alb-dns>.amazonaws.com
2..You should see your Flask app running successfully!
3.Enable ECS Auto Scaling (optional):
Scale tasks based on CPU or Memory utilization.
📊 Key Takeaways
🚀 Serverless Containers: Run Docker apps without managing EC2 instances.
⚙️ End-to-End Automation: CI/CD ensures quick, error-free deployments.
🌍 Scalability & Reliability: ALB handles routing, health checks, and scaling.
🔍 Monitoring: Integrated CloudWatch logging for observability.

🧠 Enhancements
1.Add AWS Secrets Manager for secure credentials.
2.Integrate HTTPS (ACM Certificate) on ALB.
3.Extend pipeline with test & approval stages.
4.Add SNS Notifications for build/deploy events.
📸 Suggested Images for README

1.architecture-diagram.png → Overall AWS flow
2.pipeline-overview.png → CodePipeline stages visual
3.ecs-service.png → ECS task running view
4.alb-dashboard.png → Health check status view

(Place all images in a /images folder and reference them in markdown)

🏁 Final Architecture Summary
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│   GitHub     │ ───▶ │ CodePipeline  │ ───▶ │ CodeBuild     │
└──────────────┘        └──────────────┘        └────┬─────────┘
                                                      │ Push
                                                      ▼
                                               ┌──────────────┐
                                               │ Amazon ECR   │
                                               └────┬─────────┘
                                                    │ Deploy
                                                    ▼
                                             ┌──────────────┐
                                             │ ECS Fargate  │
                                             └────┬─────────┘
                                                  │
                                                  ▼
                                             ┌──────────────┐
                                             │ Application  │
                                             │ LoadBalancer │
                                             └────┬─────────┘
                                                  ▼
                                             ┌──────────────┐
                                             │    Users     │
                                             └──────────────┘


🎯 End Result:
A fully automated, serverless CI/CD pipeline deploying your containerized app to AWS ECS Fargate — scalable, secure, and production-ready.
Developed by: Srinivas Allibilli
LinkedIn: www.linkedin.com/in/srinivas-allibilli
GitHub:
