#!/bin/bash

rep="https://github.com/lodash/lodash"
rep_clone="./repo2-temp"

git clone --quiet "$rep" "$rep_clone"
cd "$rep_clone" || { echo "Fail"; exit 1; }

tags=$(git tag)
new_tag=$(git describe --tags $(git rev-list --tags --max-count=1))
echo "Latest Tag: $new_tag"


rel=$(echo "$new_tag" | grep -o '\d+\.\d+\.\d+')
echo "Release: $rel"

mv=$(awk -F"'" '/^version /{print $2}' build.gradle)
echo "MV: $mv"

if [ "$mv" == "$rel" ] || [ "$mv" == "$new_tag" ]; then
  git tag -d "$new_tag" && git tag -d "$rel"
  git push --delete origin "$new_tag" && git push --delete origin "$rel"
  git tag "$new_tag" && git tag "$rel"
  git push origin "$new_tag" && git push origin "$rel"
else
  mv=$rel
  echo "Updated module v: $mv"
fi
