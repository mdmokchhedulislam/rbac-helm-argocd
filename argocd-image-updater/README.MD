# install arogcd image updater
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/manifests/install.yaml


# verify pods is running 
kubectl -n argocd get pods -l app.kubernetes.io/name=argocd-image-updater