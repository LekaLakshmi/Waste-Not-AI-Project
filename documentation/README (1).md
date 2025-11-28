# WasteNot: AI Ingredient Detection & Recipe Recommendation System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-EfficientNet-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-red)
![Grafana](https://img.shields.io/badge/Dashboard-Grafana-yellow)

---

## 1. Project Title and Overview

### Project Title
**WasteNot** — AI-Powered Ingredient Detection & Recipe Recommendation System

### Introduction
WasteNot is an intelligent food management system designed to tackle the growing problem of household food waste. By leveraging advanced deep learning techniques, the system identifies food ingredients from user-uploaded images and automatically suggests relevant recipes that can be prepared using those ingredients.

### Objectives
- **Reduce Food Waste:** Help users utilize ingredients they already have before they spoil
- **Simplify Meal Planning:** Automatically suggest recipes based on available ingredients
- **Demonstrate AI Lifecycle:** Showcase a complete machine learning pipeline from model development to deployment and monitoring
- **Enable Real-time Monitoring:** Provide comprehensive metrics and dashboards for system performance tracking

### Problem Statement
According to the USDA, approximately 30-40% of food in the United States goes to waste. A significant portion of this waste occurs at the household level, often because people forget what ingredients they have or don't know what to cook with them. WasteNot addresses this problem by providing an intuitive interface where users can simply upload photos of their ingredients and receive instant recipe recommendations.

### Key Features
- **Image-based Ingredient Detection:** Upload photos of ingredients for automatic identification
- **Deep Learning Model:** Utilizes EfficientNet architecture for accurate food classification
- **Smart Recipe Recommendations:** Matches detected ingredients with a curated recipe database
- **User Feedback System:** Collects user feedback to continuously improve predictions
- **Real-time Monitoring:** Prometheus and Grafana integration for performance tracking
- **Containerized Deployment:** Docker-based setup for easy deployment and scalability

---

## 2. Repository Contents

Below is the complete structure and purpose of each folder in this repository:

### `src/`
Core system code containing the main application logic:

| File/Folder | Description |
|-------------|-------------|
| `app.py` | Main application script with Gradio interface |
| `models/` | Trained EfficientNet model weights and architecture |
| `data/` | Recipe images, sample assets, and test data |
| `requirements.txt` | Python dependencies for the project |

### `deployment/`
Containerization and CI/CD configuration files:

| File | Description |
|------|-------------|
| `Dockerfile` | Docker image build configuration |
| `docker-compose.yml` | Multi-container orchestration (App + Prometheus + Grafana) |

### `monitoring/`
Performance monitoring and observability configuration:

| Folder | Description |
|--------|-------------|
| `prometheus/` | Prometheus configuration files (`prometheus.yml`) |
| `grafana/` | Grafana dashboard exports and provisioning configs |

### `documentation/`
Project documentation and reports:

| File | Description |
|------|-------------|
| `README.md` | This documentation file |
| `AI System project proposal template` | Initial project proposal document (PDF) |
| `Project report` | Comprehensive project report with findings |

### `videos/`
Demonstration and tutorial videos:

| File | Description |
|------|-------------|
| `system_demo.mp4` | Complete system demonstration screencast |

---

## 3. System Entry Point

### Main Script
```
src/app.py
```

This is the primary entry point for the WasteNot application. It initializes the Gradio web interface, loads the trained EfficientNet model, and handles the prediction pipeline.

### Running Locally

#### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

#### Step 1: Clone the Repository
```bash
git clone https://github.com/LekaLakshmi/WasteNot.git
cd WasteNot
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r src/requirements.txt
```

#### Step 4: Run the Application
```bash
python src/app.py
```

#### Step 5: Access the Interface
Open your browser and navigate to:
```
http://localhost:7860
```

### Running in Containerized Environment

#### Prerequisites
- Docker installed and running
- Docker Compose installed

#### Step 1: Build and Start All Services
```bash
docker-compose build --no-cache
docker-compose up
```

#### Step 2: Access Services
| Service | URL |
|---------|-----|
| Gradio App | http://localhost:7860 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

#### Step 3: Stop Services
```bash
docker-compose down
```

---

## 4. Video Demonstration

A comprehensive video demonstration of the WasteNot system is available at:

📽️ **Location:** `videos/system_demo.mp4`

### Demo Contents

The demonstration video showcases the following features and capabilities:

| Timestamp | Feature Demonstrated |
|-----------|---------------------|
| 0:00 - 1:00 | System overview and architecture |
| 1:00 - 3:00 | Ingredient image upload and detection |
| 3:00 - 5:00 | Recipe recommendation engine in action |
| 5:00 - 7:00 | Prediction pipeline walkthrough |
| 7:00 - 9:00 | Prometheus metrics endpoint demonstration |
| 9:00 - 11:00 | Grafana dashboard visualization |
| 11:00 - 12:00 | User feedback collection system |

### Key Highlights in Demo
- **Real-time Predictions:** Watch ingredients being identified in real-time
- **Confidence Scores:** See how the model provides confidence levels for predictions
- **Recipe Matching:** Observe the recipe recommendation algorithm in action
- **Metrics Collection:** View live metrics being scraped by Prometheus
- **Dashboard Visualization:** Explore the Grafana dashboards showing system health

---

## 5. Deployment Strategy

This system is deployed using **Docker** and **Docker Compose** for containerized, reproducible deployments.

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                    │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Gradio    │    │ Prometheus  │    │   Grafana   │     │
│  │    App      │◄───│   Server    │◄───│  Dashboard  │     │
│  │  :7860      │    │   :9090     │    │   :3000     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Services Overview

| Service | Port | Description |
|---------|------|-------------|
| **App Container** | 7860 | Runs Gradio interface and EfficientNet model inference |
| **Prometheus** | 9090 | Scrapes and stores application metrics |
| **Grafana** | 3000 | Provides visual dashboards and analytics |

### Dockerfile Details

The application Dockerfile is located at:
```
deployment/Dockerfile
```

Key Dockerfile features:
- Based on Python 3.8 slim image for minimal footprint
- Multi-stage build for optimized image size
- Health checks for container orchestration
- Non-root user for security best practices

### Build Commands

#### Build All Images
```bash
docker-compose build --no-cache
```

#### Build Individual Service
```bash
docker-compose build app
```

#### Start Services in Detached Mode
```bash
docker-compose up -d
```

#### View Logs
```bash
docker-compose logs -f
```

#### Scale Services (if needed)
```bash
docker-compose up --scale app=3
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `./models/efficientnet.h5` | Path to trained model |
| `PROMETHEUS_PORT` | `9090` | Prometheus server port |
| `GRAFANA_PORT` | `3000` | Grafana dashboard port |
| `APP_PORT` | `7860` | Gradio application port |

---

## 6. Monitoring and Metrics

### Tools Used

| Tool | Purpose | Version |
|------|---------|---------|
| **Prometheus** | Time-series metric collection and storage | 2.x |
| **Grafana** | Visualization and dashboard creation | 9.x |
| **prometheus_client** | Python instrumentation library | 0.14+ |

### Prometheus Configuration

Configuration file location:
```
monitoring/prometheus/prometheus.yml
```

#### Sample Configuration
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'wastenot-app'
    static_configs:
      - targets: ['app:7860']
    metrics_path: /metrics
```

### Metrics Monitored

The following metrics are tracked and monitored:

| Metric Name | Type | Description |
|-------------|------|-------------|
| `predictions_total` | Counter | Total number of predictions made per ingredient |
| `prediction_latency_seconds` | Histogram | Time taken for model inference |
| `prediction_confidence` | Gauge | Confidence score of predictions |
| `feedback_total` | Counter | User feedback count (Good/Bad) |
| `feedback_comments` | Counter | Number of feedback comments with unique IDs |
| `active_users` | Gauge | Currently active user sessions |
| `model_load_time` | Gauge | Time taken to load the model |

### Grafana Dashboard Setup

#### Step 1: Access Grafana
Navigate to `http://localhost:3000`

#### Step 2: Default Credentials
- **Username:** admin
- **Password:** admin

#### Step 3: Add Prometheus Data Source
1. Go to Configuration → Data Sources
2. Click "Add data source"
3. Select "Prometheus"
4. Set URL to `http://prometheus:9090`
5. Click "Save & Test"

#### Step 4: Import Dashboard
Dashboard exports are available at:
```
monitoring/grafana/dashboards/
```

### Sample Dashboard Panels

| Panel | Visualization | Metric |
|-------|---------------|--------|
| Predictions Over Time | Time Series | `predictions_total` |
| Average Latency | Gauge | `prediction_latency_seconds` |
| Confidence Distribution | Histogram | `prediction_confidence` |
| Feedback Summary | Pie Chart | `feedback_total` |

---

## 7. Project Documentation

### Key Documentation Files

| Document | Location | Description |
|----------|----------|-------------|
| **AI System Project Proposal** | `documentation/AI System project proposal template` | Initial project proposal outlining objectives, methodology, and expected outcomes |
| **Project Report** | `documentation/Project report` | Comprehensive final report with implementation details, results, and analysis |

### Documentation Contents

#### AI System Project Proposal
- Problem statement and motivation
- Proposed solution architecture
- Dataset description
- Model selection rationale
- Expected deliverables
- Timeline and milestones

#### Project Report
- Executive summary
- Literature review
- System architecture design
- Model development and training
- Evaluation metrics and results
- Deployment strategy
- Monitoring implementation
- Conclusions and future work

---

## 8. Version Control and Team Collaboration

### Git Workflow

This repository follows standard Git version control practices with a structured branching strategy:

#### Branch Structure
| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch for features |
| `feature/*` | Individual feature development |
| `bugfix/*` | Bug fixes |
| `release/*` | Release preparation |

### Commit Conventions

We follow conventional commit messages:
```
<type>(<scope>): <description>

Examples:
feat(model): add EfficientNet architecture
fix(api): resolve prediction endpoint timeout
docs(readme): update deployment instructions
```

### Code Review Process

1. **Create Feature Branch:** Branch off from `develop`
2. **Implement Changes:** Make commits with clear messages
3. **Push and Create PR:** Open pull request to `develop`
4. **Code Review:** Team members review changes
5. **Address Feedback:** Make requested changes
6. **Merge:** Squash and merge after approval

### Team Collaboration Tools

| Tool | Purpose |
|------|---------|
| GitHub Issues | Task tracking and bug reporting |
| GitHub Projects | Sprint planning and progress tracking |
| Pull Requests | Code review and collaboration |
| GitHub Actions | CI/CD automation (if applicable) |

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests as needed
5. Submit a pull request
6. Wait for review and address feedback

---

## 9. Components Not Applicable

This section addresses components from the standard template that may not be fully utilized in this project:

| Component | Status | Explanation |
|-----------|--------|-------------|
| Kubernetes | Not Used | Docker Compose was chosen for simpler deployment suitable for the project scope. Kubernetes would be considered for production-scale deployments. |
| CI/CD Pipeline | Partial | Basic Docker builds are automated; full CI/CD with GitHub Actions is planned for future iterations. |
| Load Balancing | Not Implemented | Single-instance deployment is sufficient for demonstration purposes. |
| Database Integration | Not Used | Recipe data is stored in static files; database integration is a planned future enhancement. |
| Authentication | Not Implemented | The demo version is open access; authentication would be added for production deployment. |

### Future Enhancements

The following features are planned for future releases:
- Kubernetes deployment configuration
- Full CI/CD pipeline with automated testing
- User authentication and session management
- Database integration for recipe storage
- Mobile application interface
- Multi-language support

---

## 10. Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Port 7860 already in use | Change port in `docker-compose.yml` or stop conflicting service |
| Model fails to load | Ensure model file exists in `src/models/` directory |
| Prometheus not scraping | Check network connectivity and verify `prometheus.yml` configuration |
| Grafana shows no data | Verify Prometheus data source is correctly configured |
| Docker build fails | Clear Docker cache with `docker system prune` and rebuild |

### Getting Help

If you encounter issues not covered above:
1. Check existing GitHub Issues
2. Create a new issue with detailed description
3. Include error logs and environment details

---

## 11. License

This project is developed for educational purposes as part of an AI Systems course.

---

## 12. Contact

**Maintained by:** Leka Lakshmi

📧 **GitHub Profile:** [https://github.com/LekaLakshmi](https://github.com/LekaLakshmi)


---

*Last Updated: 2024*
