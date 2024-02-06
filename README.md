# Campus Compass API

## Overview

Campus Compass API is a backend service designed to provide comprehensive information about educational institutions. This API is built with Python, using FastAPI as the web framework, SQLAlchemy for database interactions, and Alembic for database migrations.

## Repository Structure

- **`app/`**: The core directory where the FastAPI application is located.
  - **`crud/`**: Contains CRUD operation functions, interacting with the database for data manipulation.
  - **`db/`**: Houses database configuration, models, and migration scripts, defining the database schema.
  - **`etl/`**: Contains scripts for Extract, Transform, Load processes, populating the database from external sources.
  - **`schemas/`**: Defines Pydantic models for request and response data validation, ensuring data adheres to a specified format.
  - **`settings.py`**: Configuration settings for the app, including environment-specific settings.
  - **`main.py`**: Entry point of the FastAPI application, including the app instance and routes.

- **`alembic/`**: Alembic configurations for database migrations.

- **`Dockerfile`**: Docker configuration file to containerize the application.

- **`docker-compose.yml`**: Orchestrates multi-container Docker applications, managing services like the app and database.

- **`requirements.txt`**: Lists all package dependencies, installable via `pip install -r requirements.txt`.

- **`tests/`**: Test cases and suites for ensuring API functionality, crucial for CI processes and code quality.

- **`alembic.ini`**: Configuration file for managing database migrations with Alembic.


## Getting Started

Here's how you can set up your development environment:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/campuscompass-api.git
   cd campuscompass-api
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Docker Containers** (optional):
   ```bash
   docker-compose up -d
   ```

5. **Start the FastAPI Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Contribution

- **Routes**: Implementing and refining FastAPI routes for various functionalities.
- **Testing**: Developing a comprehensive test suite to ensure reliability and performance.
- **Database Setup**: Finalizing the database configurations, models, and setting up the initial database.

## Community and Support

- **Issues**: If you find any bugs or have feature requests, please open an issue in the repository.

We welcome contributions from everyone, whether you are new to the project or a seasoned contributor. Your insights and code contributions will help make Campus Compass API an invaluable tool for accessing educational institution data.

---

*Thank you for considering contributing to Campus Compass API, and we look forward to your valuable contributions!*