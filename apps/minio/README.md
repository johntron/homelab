## Installing

```shell
helm install \
  --namespace minio-operator \
  --create-namespace \
  operator minio-operator/operator
```

## Updating

```shell
helm repo add minio-operator https://operator.min.io
helm search repo minio-operator
# See https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html
```