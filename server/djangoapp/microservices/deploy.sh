#!/usr/bin/env bash
set -euo pipefail

# ========= CONFIG =========
API_KEY="${IBMCLOUD_API_KEY:-}"   # set env IBMCLOUD_API_KEY or paste below
REGION="us-south"
RESOURCE_GROUP="Default"
NAMESPACE="cardealershipsapp"
IMAGE_NAME="sentiment-backend"
CE_APP_NAME="sentianalyzer"
CE_PROJECT="$NAMESPACE"           # change if your CE project name differs
# ==========================

pause() { echo; read -r -p "✅ Step complete. Press ENTER to continue..."; echo; }

if [[ -z "$API_KEY" ]]; then
  read -r -p "Enter your IBM Cloud API key: " API_KEY
fi

echo "🔐 Logging into IBM Cloud..."
ibmcloud login --apikey "$API_KEY" -r "$REGION" -g "$RESOURCE_GROUP"
pause

echo "🔐 Logging into IBM Container Registry..."
ibmcloud cr login
pause

echo "🚧 Building Docker image..."
docker build -t "$IMAGE_NAME" .
pause

FULL_IMAGE_PATH="us.icr.io/$NAMESPACE/$IMAGE_NAME:latest"
echo "🏷️ Tagging image as $FULL_IMAGE_PATH ..."
docker tag "$IMAGE_NAME" "$FULL_IMAGE_PATH"
pause

echo "☁️ Pushing image to IBM Container Registry..."
docker push "$FULL_IMAGE_PATH"
pause

echo "🔑 Ensuring Code Engine can pull from Container Registry (idempotent)..."
ibmcloud iam authorization-policy-create container-registry codeengine "Container Registry Manager" || true
pause

echo "📁 Selecting Code Engine project..."
ibmcloud ce project select -n "$CE_PROJECT"
pause

echo "🚀 Deploying/Updating Code Engine app..."
if ibmcloud ce application get -n "$CE_APP_NAME" >/dev/null 2>&1; then
  ibmcloud ce application update -n "$CE_APP_NAME" --image "$FULL_IMAGE_PATH" --registry-secret icr-secret --port 5000
else
  ibmcloud ce application create -n "$CE_APP_NAME" --image "$FULL_IMAGE_PATH" --registry-secret icr-secret --port 5000
fi
pause

echo "🌐 App URL:"
ibmcloud ce application get -n "$CE_APP_NAME" --output url || true
echo
read -r -p "✅ All done. Press ENTER to exit..."
