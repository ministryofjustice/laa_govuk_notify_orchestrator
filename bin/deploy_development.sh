#!/usr/bin/env bash
set -e

ROOT=$(dirname "$0")
HELM_DIR="$ROOT/../helm_deploy/laa-govuk-notify-orchestrator/"

helm upgrade laa-govuk-notify-orchestrator \
  $HELM_DIR \
  --namespace=$NAMESPACE \
  --values ${HELM_DIR}/values-development.yaml \
  --set image.repository=$REGISTRY_HOST \
  --set image.tag=$CIRCLE_SHA1 \
  --install
