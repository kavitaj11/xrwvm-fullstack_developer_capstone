#!/bin/bash

echo "🚀 Creating Registry Secret (if not exists)..."
ibmcloud ce secret create \
  --name icr-secret \
  --format registry \
  --server us.icr.io \
  --username iamapikey \
  --password JUp_6KQoeATnntDTYIBLA08QUhdZ3bLOlqckMVbj94sr

echo "🚀 Creating Code Engine App..."
ibmcloud ce app create \
  --name dealership \
  --image us.icr.io/cardealershipsapp/ibm-fullstack_developer_capstone:latest \
  --registry-secret icr-secret \
  --cpu 0.25 \
  --memory 1G \
  --port 8000

echo "✅ App created. Updating command to run Gunicorn..."
ibmcloud ce app update \
  --name dealership \
  --cmd "sh -c 'gunicorn server.wsgi:application --bind 0.0.0.0:8000; sleep infinity'"

echo ""
echo "✅ Deployment finished."
echo "🔍 View logs using: ibmcloud ce app logs -f --name dealership"
echo ""

read -p "Press ENTER to exit the script."
