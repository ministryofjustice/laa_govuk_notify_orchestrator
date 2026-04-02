#!/usr/bin/env bash
set -e

HELM_DIR="./helm_deploy/laa-govuk-notify-orchestrator"

helm upgrade laa-govuk-notify-orchestrator \
  $HELM_DIR \
  --namespace=$NAMESPACE \
  --values ${HELM_DIR}/values-$ENVIRONMENT.yaml \
  --set image.repository=$REGISTRY_HOST \
  --set image.tag=$IMAGE_TAG \
  --install
