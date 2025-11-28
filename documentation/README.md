# WasteNot: AI Ingredient Detection & Recipe Recommendation System
## 1. Project Title and Overview
WasteNot is an AI-powered ingredient detection and recipe recommendation system designed to reduce food waste and help users cook efficiently with the ingredients they already have. The system identifies food items from uploaded images using a deep learning model (EfficientNet) and suggests relevant recipes automatically. It demonstrates a complete AI lifecycle including model development, containerized deployment, monitoring, and feedback integration.
---
## 2. Repository Contents
Below is the structure and purpose of each folder in this repository:
### `src/`
Core system code, including:
- `app.py` — main application script
- `models/` — trained EfficientNet model
- `data/` — recipe images and sample assets
- `requirements.txt` — Python dependencies
### `deployment/`
Containerization and CI/CD configuration:
- `Dockerfile` — builds the application image
- `docker-compose.yml` — multi-container setup (App + Prometheus + Grafana)
### `monitoring/`
Performance monitoring configuration:
- `prometheus/` — Prometheus configuration file
- `grafana/` *(optional)* — dashboard exports (if added later)
### `documentation/`
Project documentation:
- `README.md` — this file
- AI System Project Proposal (PDF)
- Additional reports (if applicable)
### `videos/`
Contains the demo screencast demonstrating the system:
- `system_demo.mp4`
---
## 3. System Entry Point
### Main script:
``src/app.py``
### Instructions to run locally
Install dependencies:
``pip install -r src/requirements.txt``
Run the app:
``python src/app.py``
The Gradio interface launches at:
``http://localhost:7860``
---
## 4. Video Demonstration
A full working demo of the system is available here:
📽️ `videos/system_demo.mp4`
The demo showcases:
- Ingredient image upload
- Prediction pipeline
- Recipe recommendation engine
- Prometheus metrics endpoint
- Grafana visual dashboard
---
## 5. Deployment Strategy
This system is deployed using **Docker** and **Docker Compose**.
### Build and Start Containers
From the root folder:
``docker-compose build --no-cache``
``docker-compose up``
### Services included:
- **App Container:** Runs the Gradio interface and model inference
- **Prometheus:** Scrapes model metrics
- **Grafana:** Displays live dashboards
Refer to:
``deployment/Dockerfile``
---
## 6. Monitoring and Metrics
### Tools Used
- **Prometheus** — metric scraping
- **Grafana** — dashboards and visual analytics
- **prometheus_client** — Python instrumentation library
### Metrics Monitored
- Total predictions per ingredient
- Prediction latency
- Confidence scores
- User feedback (“Good” / “Bad”)
- Feedback comments (with unique IDs)
Prometheus config:
``monitoring/prometheus/prometheus.yml``
---
## 7. Project Documentation
### Key Files:
- **AI System Project Proposal:** `documentation/AI System project proposal template`
- **Project Report (optional):** `documentation/Project report`
These documents describe the system architecture, model development, and evaluation details.
---
## 8. Version Control and Team Collaboration
This repository follows standard Git version control practices:
- Frequent commits during different project stages
- Branching for new features
- Merge strategy to maintain clean main branch
Team collaboration includes shared issue tracking and version-controlled documents.
---


## 📬 Contact
Maintained by **Leka Lakshmi**
GitHub Profile: https://github.com/LekaLakshmi
