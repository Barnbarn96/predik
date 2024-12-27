# Flask App Deployment with Podman and Kubernetes

This README provides the steps to build, push, deploy, and port-forward a Flask application using **Podman** and **Kubernetes**.

## Prerequisites

- **Podman** installed on your local machine for building and pushing the Docker image.
- **Kubernetes** (minikube, kubeadm, or any local cluster setup) to deploy the application.
- **kubectl** installed for interacting with the Kubernetes cluster.

---

## Steps

### 1. Build and Push Docker Image with Podman

First, build and push the Flask app Docker image using **Podman**.

```bash
# Tag the local image for the Docker registry
podman tag flask-app:latest docker.io/barnbarn96/predik-epl:latest

# Push the tagged image to the Docker registry
podman push docker.io/barnbarn96/predik-epl:latest



# Apply the Kubernetes deployment file (e.g., kubernetes.yaml)
kubectl apply -f kubernetes.yaml


$podName = kubectl get pods --no-headers | Select-String "flask" | ForEach-Object { $_.Line.Split(' ')[0] }

kubectl port-forward pod/$podName 8080:8080
