kubectl delete secret icr-secret --ignore-not-found=true

kubectl create secret docker-registry icr-secret \
  --docker-server=us.icr.io \
  --docker-username=iamapikey \
  --docker-password=<API-Key> \
  --docker-email=kavita.jadhav1109@gmail.com