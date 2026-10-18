# Django CRM Deployment

A containerized deployment of Django CRM, an open source customer
relationship management application built with Django
(https://github.com/DjangoCRM/django-crm).

This project takes the CRM from a local Docker Compose setup all the way to
a Kubernetes cluster. It includes a Dockerfile for the application, a Compose
stack with MySQL, Ansible playbooks to automate setup, a Jenkins pipeline
that builds and publishes the image to a private Gitea registry, and
Kubernetes manifests to run it on a cluster.


## Features

- Builds the Django CRM into a lightweight Python Alpine container image
- Runs the full stack locally with one command: the CRM, MySQL and Adminer
- Automates environment setup with Ansible
- Continuous integration with Jenkins: every build is tagged with the build
  number and commit hash and pushed to a Gitea container registry
- Deploys to Kubernetes with Kustomize, including a namespace, deployment,
  NodePort service and health checks
- Runs database migrations automatically when the container starts
- Ready to use in a VS Code dev container


## Tech Stack

    Application        Django CRM (Python, Django)
    Database           MySQL
    Database UI        Adminer
    Containers         Docker, Docker Compose
    Automation         Ansible
    CI                 Jenkins
    Image registry     Gitea container registry
    Orchestration      Kubernetes, Kustomize


## Project Structure

    Dockerfile              Builds the CRM image
    docker-compose.yml      Runs the CRM, MySQL and Adminer locally
    settings.py             Django settings configured for this setup
    patch-settings.diff     Patch that applies this setup's changes to the upstream settings
    up.yml                  Ansible playbook that starts the stack and installs tools
    down.yml                Ansible playbook that stops the stack
    Jenkinsfile             CI pipeline that builds and pushes the image
    k8s/                    Kubernetes manifests (namespace, deployment, service, kustomization)
    schema_changes.sql      Sample SQL script that creates test databases
    .devcontainer/          Dev container configuration
    LICENSE                 MIT License


## Architecture

    Developer push
          |
          v
    Jenkins pipeline  --->  builds Docker image  --->  pushes to Gitea registry
                                                              |
                                                              v
                                               Kubernetes pulls the image
                                               and runs it in the django-crm
                                               namespace (NodePort 32080)

Locally, Docker Compose runs:

    crm                  Django CRM on http://localhost:8080
    db                   MySQL (database crm_db), data stored in the mysql_db_data volume
    adminer_container    Adminer on http://localhost:8078


## Getting Started

### Prerequisites

- Docker with the Compose plugin
- Ansible, with the community.docker collection
- Git
- kubectl and access to a cluster (for the Kubernetes deployment)

### 1. Clone the repository and the CRM source

    git clone <this-repository-url>
    cd django-crm
    git clone https://github.com/DjangoCRM/django-crm.git django-crm

### 2. Configure your hostname

Edit settings.py in the repository root so that ALLOWED_HOSTS and
CSRF_TRUSTED_ORIGINS contain the host you will use to reach the CRM:

    ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-host.example.com']
    CSRF_TRUSTED_ORIGINS = ['https://your-host.example.com']

The database HOST is already set to db, the name of the MySQL service in
docker-compose.yml. The Docker build copies this settings.py into the image
automatically. patch-settings.diff shows the changes made to the upstream
settings file.

### 3. Start the stack

    ansible-playbook up.yml

This starts the containers and installs the MySQL client and Python MySQL
connectors. You can also run docker compose up -d directly.

### 4. Create the superuser (first run only)

    docker compose exec crm sh -c "python manage.py setupdata"

This prints a superuser name and password. Save them, because they cannot be
retrieved again.

### 5. Open the application

    Admin site:   http://localhost:8080/en/456-admin/
    CRM site:     http://localhost:8080/en/123/
    Adminer:      http://localhost:8078/  (server: db)

To stop everything, run ansible-playbook down.yml or docker compose down.


## Continuous Integration

The Jenkinsfile runs three stages:

1. Checkout: checks out the code and works out a build tag in the form
   <build number>-<short commit hash>.
2. Build: builds the Docker image and tags it with the build tag and latest.
3. Push: logs in to the Gitea registry and pushes both tags.

After each run, the pipeline logs out of the registry and removes the local
images to keep the build agent clean.

Configuration at the top of the Jenkinsfile:

    REGISTRY_INTERNAL      LAN address of the Gitea registry used for pushing
    REGISTRY_PUBLIC        Public address of the registry used for pulling
    OWNER / IMAGE_NAME     Registry owner and image name
    DOCKER_CREDENTIALS_ID  Jenkins username/password credential for the registry


## Kubernetes Deployment

Create the image pull secret for the private registry:

    kubectl create namespace django-crm
    kubectl -n django-crm create secret docker-registry regcred \
      --docker-server=<registry-host> \
      --docker-username=<user> \
      --docker-password=<token>

Deploy the application:

    kubectl apply -k k8s/

The CRM is then available at http://<node-ip>:32080/. The deployment needs a
MySQL server that the pod can reach under the hostname set in settings.py.


## Notes and Next Steps

- The passwords, SECRET_KEY and DEBUG = True in this repository are for
  development only. Move them to environment variables or Kubernetes
  secrets before going to production.
- Planned: a Helm chart, persistent NFS storage for MySQL, and a Cloudflare
  tunnel to expose the CRM to the internet.


## License

MIT License. See the LICENSE file.
