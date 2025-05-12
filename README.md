# 🧑‍⚕️ Backend - Patient Visit Dashboard

A Django-based backend service for managing patient data and visit history. It exposes APIs that can be consumed by a frontend like Next.js.

## ⚙️ Setup Instructions

## 🧰 Tech Stack

- [Python 3.12+](https://www.python.org/)
- [Django 5.x+](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the Repository

```bash
git clone https://github.com/ThunderMind2019/sarc_medic_be
cd sarc_medic_be
```

### 2. Build and Run with Docker
```bash
docker-compose up --build
```

## Extra Notes

### Background Task Handling (Celery Integration)

If the application needs to process large files, doing so within a standard HTTP request can lead to timeouts and poor user experience.

To handle such scenarios efficiently, we can integrate:

- Celery for background task processing

- Redis or RabbitMQ as the message broker

- Optional: Django Channels, WebSockets, or email notifications for user updates
