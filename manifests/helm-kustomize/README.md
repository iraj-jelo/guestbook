# Helm and Kustomize

This setup uses Kustomize to render the local Helm chart and apply the
environment-specific namespace and replica counts. The base chart defaults
match the manifests; the overlays match the dev, staging, and prod replica
counts.

Requirements: `kubectl` with Kustomize support and Helm installed.

Build an environment's manifests:

```sh
kubectl kustomize --enable-helm --load-restrictor LoadRestrictionsNone manifests/helm-kustomize/overlays/dev
```

Apply an environment:

```sh
kubectl kustomize --enable-helm --load-restrictor LoadRestrictionsNone manifests/helm-kustomize/overlays/dev | kubectl apply -f -
```

Use `staging` or `prod` in place of `dev` to build or apply the other
environments. The load restriction is disabled because the base references the
existing Helm chart outside `helm-kustomize`. The rendered resources create
their namespace, so no separate namespace creation command is needed.
