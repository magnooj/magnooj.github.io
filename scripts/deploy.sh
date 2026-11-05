#!/bin/sh
# GitHub Actions builds and publishes the site (.github/workflows/deploy.yml): on every push to main,
# and every morning so scheduled posts go live on their date. This starts a run by hand,
# for example to publish again right away. It publishes what is on main, not local changes.
set -e
gh workflow run deploy.yml --repo magnooj/magnooj.github.io --ref main
echo "Started. Follow it at https://github.com/magnooj/magnooj.github.io/actions"
