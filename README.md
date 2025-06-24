<h1>DevOps Internship Project: Go, Python, and Nginx Microservices<h1>
This repository contains a simple microservices application demonstrating containerization with Docker and orchestration with Docker Compose. It features:

A backend service written in Go (Service 1).

A backend service written in Python Flask (Service 2).

An Nginx reverse proxy to route requests to the appropriate backend service.

🚀 Setup Instructions
Follow these steps to get the application up and running on your local machine or a cloud instance (like EC2) with Docker installed.

Prerequisites
Install below softwares:
docker
docker-compose
Git

Deployment Steps
Clone the Repository:

git clone https://github.com/GaniDynamo/devops-internship-project.git
cd devops-internship-project

Build and Run the Services using Docker Compose:
Navigate to the root of the cloned repository (where docker-compose.yml is located) and run:

docker-compose up --build -d

--build: Forces a rebuild of images, ensuring the latest changes (e.g., curl installation) are applied.

-d: Runs the containers in detached mode (in the background).

Verify Services Status:
Wait for about 30-40 seconds to allow all services to start and health checks to pass. Then check their status:

docker-compose ps

You should see Up (healthy) for service1 and service2, and Up for nginx.

Accessing the Application
Once all services are running healthy, you can access the application through the Nginx reverse proxy.

If running locally:

Go Service: http://localhost:8080/service1

Python Service: http://localhost:8080/service2

If running on an EC2 instance:
Replace YOUR_EC2_PUBLIC_IP with the Public IPv4 address of your EC2 instance.

Go Service: http://YOUR_EC2_PUBLIC_IP:8080/service1

Python Service: http://YOUR_EC2_PUBLIC_IP:8080/service2

🚦 How Routing Works (Nginx Reverse Proxy)
Nginx acts as a reverse proxy, directing incoming web requests to the appropriate backend microservice based on the URL path.

docker-compose.yml:

The nginx service exposes port 8080 of the host machine to port 80 inside the Nginx container ("8080:80"). All external traffic for this application comes in through host port 8080.

service1 and service2 are exposed on internal ports (8001 and 8002 respectively) within the Docker network, but these ports are not directly exposed to the host machine, meaning they are only accessible from other containers within the same Docker Compose network (like Nginx).

nginx/nginx.conf:
This configuration file defines how Nginx handles requests:

It listens on port 80 (inside the Nginx container).

Requests to /service1 are proxied to http://service1:8001/hello. service1 is the Docker Compose service name, which resolves to the internal IP address of the Go application container. The /hello endpoint is specifically targeted as per the Go service's implementation.

Requests to /service2 are proxied to http://service2:8002/hello. Similarly, service2 resolves to the Python application container, hitting its /hello endpoint.

Any other requests (/) will return a 404 Not Found error.

This setup allows a single entry point (Nginx) to manage traffic for multiple backend services, providing load balancing capabilities, SSL termination (if configured), and centralizing access control.

✨ Bonus Features Implemented
This project incorporates several best practices and features for a robust and maintainable Dockerized microservice architecture:

Logging Clarity (json-file driver)

Each service (nginx, service1, service2) is configured in docker-compose.yml to use the json-file logging driver.

max-size: "10m": Limits log files to 10 MB.

max-file: "3": Rotates logs, keeping up to 3 files.

This ensures that logs don't consume excessive disk space and are easily manageable for debugging and monitoring. You can view logs using docker-compose logs <service_name>.

Clean and Modular Docker Setup

Separate Dockerfiles: Each service (service_1, service_2, nginx) has its own Dockerfile in its dedicated subdirectory. This promotes modularity, allowing each service to be built independently with its specific dependencies and build process.

Build Contexts: docker-compose.yml uses context: ./<service_folder> to define the build context for each service, ensuring that only necessary files are included in the build, leading to smaller and more secure images.

Healthcheck for Automated Testing and Reliability

healthcheck configurations are defined in docker-compose.yml for service1 and service2.

Test Command: ["CMD", "curl", "-f", "http://localhost:<port>/ping"]

This command checks if the /ping endpoint of each service is reachable and returns a success (2xx) status code. The -f flag makes curl fail for HTTP errors (e.g., 4xx, 5xx).

curl was explicitly installed in both Go and Python Dockerfiles to ensure the health check command is available inside the minimal images.

interval: 10s: Checks the health every 10 seconds.

timeout: 10s: Gives the health check 10 seconds to respond.

retries: 3: If a check fails, it retries 3 times before marking the service as unhealthy.

start_period: 30s: Provides an initial grace period of 30 seconds after container startup before health checks begin, preventing services from being marked unhealthy while they are still initializing.

depends_on with condition: service_healthy: Nginx will only start once both service1 and service2 are reported as healthy by their respective health checks. This ensures proper startup order and avoids Nginx trying to proxy to non-existent or unresponsive backends.

📅 Deadline Acknowledged
This project was developed within the requested timeframe.
