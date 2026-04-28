#!/bin/bash

echo "Updating Helm values"

sed -i "s/tag:.*/tag: \"$IMAGE_TAG\"/" devops-platform/values.yaml

git config --global user.email ci@company.com
git config --global user.name ci-bot

git add devops-platform/values.yaml
git commit -m "update backend image to $IMAGE_TAG" || echo "no changes"

git push https://$GITHUB_TOKEN@github.com/amankumar0806/Project.git HEAD:main