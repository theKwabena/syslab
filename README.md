# SYSLAB - LINUX PLAYGROUND
This project is designed to provide an interactive environment for practicing Linux commands through a web-based interface. It consists of a Python backend and a Vue.js frontend built with Nuxt.js. When a user logs in, a Docker container is spawned, allowing commands to be sent to it, with results displayed on the screen.

## Features
- User Authentication: Secure login to access the interactive shell.
- Docker Integration: Spawns a Docker container on login, isolating user environments.
- Command Execution: Sends Linux commands to the container and displays results in real-time.
- Responsive Frontend: Built with Nuxt.js for a seamless user experience.
  
## Tech Stack
- Frontend: Nuxt.js (Vue.js)
- Backend: Python (FastAPI)
- Containerization: Docker
- Database: SQLite or any database of your choice for user management (optional)

## Getting Started

### Prerequisites
- Docker installed on your machine.

### Installation 
1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/linux-practice-project.git
   cd linux-practice-project
      
2. **Configure Environment Variables**:
   Create a .env file in the root of the project with the following variables:
     
     ```
    ADMIN_PASSWORD - Password for the admin user
    ADMIN_USER - The first admin user for user management
    PROJECT_NAME - Name of project to display in swagger documentation
    DEFAULT_UNIX_IMAGE- Default image which containers are spawned with
    DOCKER_HOST_URL - URL for the docker host that the containers will use

    ```

3. **Start the application**
   ```
    docker compose -f deploy.yml up
   ```
