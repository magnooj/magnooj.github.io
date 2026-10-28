#!/bin/sh
# Build the site and publish _site to the gh-pages branch, which GitHub Pages serves.
set -e
cd "$(dirname "$0")/.."
npm run build
touch _site/.nojekyll
cd _site
rm -rf .git
git init -q -b gh-pages
git add -A
git -c user.name="Ali Ganjizadeh" -c user.email="76149617+magnooj@users.noreply.github.com" \
  commit -q -m "Deploy $(date -u +%Y-%m-%dT%H:%MZ)"
git -c credential.helper= -c credential.helper='!gh auth git-credential' \
  push -q -f https://github.com/magnooj/magnooj.github.io.git gh-pages
rm -rf .git
echo "Published. GitHub Pages updates in about a minute: https://magnooj.github.io"
