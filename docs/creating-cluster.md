# Create a development cluster

You need `kind` and `kubectl` installed. Create a kind configuration file named
`kind-cluster.yaml`:

```yaml
# kind-cluster.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

Create the cluster:

```bash
kind create cluster --name guestbook-cluster --config kind-cluster.yaml
```

## Install Argo CD in the cluster

Create the Argo CD namespace and install the official stable manifests:

```sh
kubectl create namespace argocd
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait for the Argo CD deployments to become available:

```sh
kubectl wait --for=condition=Available --timeout=300s \
  deployment --all -n argocd
```

The Guestbook Argo CD Applications use Kustomize to render a Helm chart. Before
creating one, enable Helm rendering in Argo CD and restart its repository
server:

```sh
kubectl apply -n argocd -f manifests/argocd/argocd-cm.yaml
kubectl rollout restart deployment/argocd-repo-server -n argocd
kubectl rollout status deployment/argocd-repo-server -n argocd
```

The repository's Argo CD configuration also enables the insecure HTTP server
mode. For local access, keep the server private and use port forwarding rather
than exposing it directly:

```sh
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Open http://localhost:8080 and obtain the initial admin password with:

```sh
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

After Argo CD is ready, apply a Guestbook Application manifest as described in
the [installation guide](../README.md#option-3-argo-cd-application).
