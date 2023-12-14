```shell
kubectl create namespace mosquitto
helm repo add k8s-at-home https://k8s-at-home.com/charts/
helm repo update
helm upgrade --install mosquitto k8s-at-home/mosquitto -f values.yaml --namespace mosquitto
```
