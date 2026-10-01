# creating a cluster

You need to have a Kubernetes cluster, and the `kubectl` command-line tool must be configured to communicate with your cluster. First we need a `Kind` manifest in order to create a cluster for dev purposes:

```yaml
# kind-cluster.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```

Then run the manifest using the `Kind` command:

```bash
kind create cluster --name guestbook-cluster --config kind-cluster.yaml
```
