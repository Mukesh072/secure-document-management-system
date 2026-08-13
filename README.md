# 🔐 Secure Document Management System Using AWS Cloud

A secure web-based document management system built with **Flask** and deployed on **Amazon EC2**, with documents stored securely in **Amazon S3**.

The system allows users to register, log in, and manage their documents through a simple web interface.

## 🚀 Live Demo

**Application:** http://13.51.7.138

> The application is deployed on AWS EC2 using Nginx and Gunicorn.

---

## 📌 Project Overview

The Secure Document Management System provides a centralized platform for users to securely manage their documents.

Users can:

- Create an account and log in
- Upload documents
- View their uploaded documents
- Download documents
- Delete documents
- Store documents securely in Amazon S3

The application uses AWS IAM to control access to AWS resources and Amazon S3 to store uploaded documents.

---

## ✨ Features

- 🔐 User Registration and Login
- 📤 Document Upload
- 📄 Document Management
- 📥 Document Download
- 🗑️ Document Delete
- ☁️ Secure Amazon S3 Storage
- 👤 IAM-based AWS access control
- 📝 Application logging
- 🌐 AWS EC2 deployment
- ⚡ Nginx reverse proxy
- 🚀 Gunicorn WSGI server

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| HTML/CSS | Frontend |
| SQLite | Database |
| Boto3 | AWS integration |
| Gunicorn | Production WSGI server |
| Nginx | Reverse proxy |
| Git | Version control |
| GitHub | Source code hosting |

---

## ☁️ AWS Services Used

### Amazon EC2

Hosts and runs the Flask application.

### Amazon S3

Stores uploaded documents separately from the application server.

### AWS IAM

Controls access between the EC2 instance and AWS services.

An IAM Role is attached to the EC2 instance so the application can access S3 without storing AWS secret keys in the project.

### Amazon CloudWatch

Used for application logging and monitoring.

---

## 🏗️ System Architecture

```text
                    Internet
                       │
                       ▼
                ┌──────────────┐
                │    AWS EC2   │
                │ 13.51.7.138  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │    Nginx     │
                │    Port 80   │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │   Gunicorn   │
                │  Port 5000   │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │    Flask     │
                │ Application  │
                └──────┬───────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
        ┌──────────┐      ┌──────────┐
        │  SQLite  │      │ Amazon   │
        │ Database │      │    S3    │
        └──────────┘      └──────────┘
                              │
                              ▼
                         AWS IAM Role
