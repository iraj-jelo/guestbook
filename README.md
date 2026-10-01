# Guestbook

**A multi-tier web application with Redis and Python (FastAPI) using Kubernetes.**

This a application is based on a [Google](https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/guestbook) and [kubernetes](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/) samples with PHP but overwritten with Python and few minor changes in deployments, services manifests to make it easier working with local Redis and frontend application images.

![diagram](diagram.png)

### creating a cluster

You need to have a Kubernetes cluster, and the kubectl command-line tool must be configured to communicate with your cluster. for creating a dev cluster using kind read [creating a cluster](./docs/creating-cluster.md).


First create a namespace for our application

```sh
kubectl create namespace guestbook
```

Build a docker image for Guestbook frontend application (`guestbook`):

```sh
cd python-redis && docker build --target runtime -t irajjelodari/guestbook:1.0.0 .
```

Load the docker images (Redis and guestbook) into your cluster nodes:

```sh
kind load docker-image 'redis:8.8.2' --name=guestbook-cluster
kind load docker-image 'irajjelodari/guestbook:1.0.0' --name=guestbook-cluster
```

Apply the manifests:

```sh
kubectl apply -n guestbook -f redis-leader-deployment.yaml
kubectl apply -n guestbook -f redis-leader-service.yaml

kubectl apply -n guestbook -f redis-follower-deployment.yaml
kubectl apply -n guestbook -f redis-follower-service.yaml

kubectl apply -n guestbook -f frontend-deployment.yaml
kubectl apply -n guestbook -f frontend-service.yaml
```

Expose the frontend service using `port-forward` command to access the application on your local machine:

```sh
kubectl port-forward -n guestbook service/frontend 8542:8000
```

![Guestbook application screenshot](screenshot.png)

### Clean-up

To clean up everything:

```sh
kubectl delete -n guestbook deployment -l app=redis
kubectl delete -n guestbook service -l app=redis
kubectl delete -n guestbook deployment frontend
kubectl delete -n guestbook service frontend

kubectl delete namespace guestbook

kind delete cluster --name guestbook-cluster
```
