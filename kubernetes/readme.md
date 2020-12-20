# Replaybot Kubernetes

Replaybot uses Kustomize to minimise duplication between environments

* `kubectl kustomize overlay/testing`
* `kubectl apply -k overlay/testing`

resource limits are conservative for the moment as im running on a small cluster
```
parser          150m    300mi
discord         100m    100mi
search          100m    100mi
elasticsearch   500m    500mi
total           850m   1000mi
```
