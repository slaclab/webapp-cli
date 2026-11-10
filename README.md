# webapp-cli

Deploy a simple web app to Kubernetes with a handful of shell scripts that
each do one thing. Nothing is hidden: every script runs `kubectl` (or
`docker`) and prints the command before executing it.

The container image is built in CI (GitHub Actions) on every push to
`main`, so day-to-day you only need the deploy / status / logs / delete
scripts.

## What's here

```
.github/workflows/build-image.yml      # CI: builds + pushes the image
program-calendar-api/
├── config.sh                          # shared variables
├── Dockerfile                         # how to build the image
├── manifests/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── app.py, base_events.py, …          # FastAPI source lives here too
├── facet/, lcls/, spear/, util/       # same
├── pyproject.toml, requirements.txt   # same
├── 1-build.sh                         # local build+push (optional; CI usually does this)
├── 2-deploy.sh                        # kubectl apply + create Secret from local files
├── 3-status.sh                        # kubectl get
├── 4-logs.sh                          # kubectl logs
└── 5-delete.sh                        # kubectl delete
```

The FastAPI source lives alongside the Dockerfile so CI can build the
image from a single checkout.

## How the pieces fit

```
   push to main ──► GitHub Actions ──► ghcr.io/slaclab/program-calendar-api:dev
                                                     │
                                                     ▼
   you run ./2-deploy.sh ──► kubectl apply ──► Pod pulls image + Secret
                                                     │
                                                     ▼
                                       kubectl port-forward ──► localhost:8080
```

## Prereqs (for deploying)

- `kubectl` configured for your cluster (we use SLAC `ad-accel-online-ml-dev`)
- `credentials.json`, `token.json`, `config.json` present in
  `program-calendar-api/` (gitignored). Generate `token.json` by running
  the app once locally and completing the Google OAuth consent in a browser.

For local image builds (optional, only if iterating faster than CI allows):
- `docker` daemon running
- `docker login ghcr.io` as a GitHub user with push rights to `slaclab/`

## Everyday workflow

```bash
# 1. Edit code, commit, push.
git add program-calendar-api/app.py
git commit -m "tweak events handler"
git push origin main
# → GitHub Actions builds and pushes ghcr.io/slaclab/program-calendar-api:dev

# 2. Deploy the new image to the cluster.
cd program-calendar-api
./2-deploy.sh
./3-status.sh
```

`imagePullPolicy: Always` on the Deployment makes the Pod re-pull the `dev`
tag on each rollout, so the push → deploy loop works without changing tags.

## Open it in a browser

```bash
kubectl -n program-calendar-dev port-forward svc/program-calendar-api 8080:80
# then open http://127.0.0.1:8080/docs
```

## Logs

```bash
./4-logs.sh          # last 200 lines
./4-logs.sh -f       # follow
```

## Delete

```bash
./5-delete.sh                # Deployment + Service + Secret (keeps namespace)
./5-delete.sh --namespace    # also removes the namespace
```

## Local build (bypass CI)

```bash
./1-build.sh         # docker build + push to ghcr.io/slaclab/program-calendar-api:dev
```

Only useful if you want to test an uncommitted change before pushing.

## Switch to a different app

Copy `program-calendar-api/` to a new directory, replace the source with
your app, edit `config.sh` and the three YAML files, and point
`build-image.yml` at the new path. That's the whole porting process.
