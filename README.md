# Guestbook

**A multi-tier web application with Redis and Python (FastAPI) using Kubernetes.**

This a application is based on a [Google](https://docs.cloud.google.com/kubernetes-engine/docs/tutorials/guestbook) and [kubernetes](https://kubernetes.io/docs/tutorials/stateless-application/guestbook/) samples with PHP but overwritten with Python and few minor changes in deployments, services manifests to make it easier working with local Redis and frontend application images.

![diagram](diagram.png)

### creating a cluster

You need to have a Kubernetes cluster, and the kubectl command-line tool must be configured to communicate with your cluster. for creating a dev cluster using kind read [creating a cluster](./docs/creating-cluster.md).


Build a docker image for Guestbook frontend application (`guestbook`):

```sh
cd python-redis && docker build --target runtime -t irajjelodari/guestbook:1.0.0 .
```

Load the docker images (Redis and guestbook) into your cluster nodes:

```sh
kind load docker-image 'redis:8.8.2' --name=guestbook-cluster
kind load docker-image 'irajjelodari/guestbook:1.0.0' --name=guestbook-cluster
```

Install the Helm chart (it creates the `guestbook` namespace):

```sh
helm install guestbook ./guestbookchart --namespace guestbook --create-namespace
```

To deploy with Kustomize overlays that render the Helm chart for dev, staging, or prod, see [helm-kustomize](./helm-kustomize/README.md).

The chart defaults match the base manifests. To use the replica counts from an environment overlay, pass its values file and namespace, for example:

```sh
helm install guestbook ./guestbookchart \
  --namespace guestbook-dev \
  --create-namespace \
  --values ./guestbookchart/values-dev.yaml
```

Use `values-staging.yaml` or `values-prod.yaml` for the other overlays. To access the application locally, forward the frontend service:

```sh
kubectl port-forward -n guestbook service/frontend 8542:80
```

Then open http://localhost:8542.

![Guestbook application screenshot](screenshot.png)

### Continuous integration

The GitHub Actions workflow runs on pushes and pull requests. It checks Python
dependencies and syntax, builds the frontend Docker image without publishing
it, and lints and renders the Helm and Kustomize configurations for dev,
staging, and prod.

### Clean-up

To remove the Helm release and clean up the namespace:

```sh
helm uninstall guestbook -n guestbook
kubectl delete namespace guestbook
kind delete cluster --name guestbook-cluster
```
