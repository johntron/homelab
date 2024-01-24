Originally downloaded using:

```shell
helm repo add blakeblackshear https://blakeblackshear.github.io/blakeshome-charts/
helm repo update
helm fetch blakeblackshear/frigate
tar -xzf frigate-7.2.0.tgz
mv frigate chart
rm frigate-7.2.0.tgz
```

Installing:

```shell
helm upgrade --install --create-namespace --namespace frigate frigate chart/ -f values.yaml
```