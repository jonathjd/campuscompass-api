# Campus Compass API

## Overview

Welcome! This repo contains a backend web API that build with FastAPI and allows users to query the [College Scorecard API](https://collegescorecard.ed.gov/data/documentation/) effeciently and quickly. Follow the getting started steps to begin contributing!


## Getting Started

Here's how you can set up your development environment:

1. **Fork** the repository on GitHub.

2. **Clone** your fork to your local machine:
   ```bash
   git clone https://github.com/your-username/campuscompass-api.git
   cd campuscompass-api/
   ```

3. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. **Create Image and Build the Docker Container**:
The api is containerized using Docker, run the below commands to build and run the containers.
   ```bash
   docker-compose build --no-cache
   docker-compose up -d # -d flag detaches from terminal
   ```

To run the application locally, run the following command-

5. **Start the FastAPI Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
The `--reload` command will dynamically reload your server with the updated changes.

## Development

1. Create a new **branch** for your development:
   ```bash
   git checkout -b feat/your-feature-branch
   ```

2. Make your changes and **test** them with pytest:
   ```bash
   pytest
   ```

3. If all tests pass **commit** them:
   ```bash
   git commit -am "Add some feature"
   ```

4. **Push** the changes to your fork:
   ```bash
   git push origin your-feature-branch
   ```

5. Submit a **Pull Request** through GitHub to the original repository.

Linting (with flake8 and black) and testing (with pytest) will be automatically applied to pull requests via GitHub Actions.

## Community and Support

- **Issues**: If you find any bugs or have feature requests, please open an issue in the repository.

We welcome contributions from everyone, whether you are new to the project or a seasoned contributor. Your insights and code contributions will help make Campus Compass API an invaluable tool for accessing educational institution data.

---

*Thank you for considering contributing to Campus Compass API, and we look forward to your valuable contributions!*