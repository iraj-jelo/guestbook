

### Docker Image

To consume the app in your Kubernetes deployment, build `gb-frontend` image by the following command:
```bash
docker build --target runtime -t gb-frontend:v1 .
```