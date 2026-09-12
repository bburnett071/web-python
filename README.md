# Austin temperature demo pipeline

Demo only. A GitHub Action runs every 4 hours (at :23 past, UTC, to avoid GitHub's congested top-of-hour cron slot) and:

1. `db_pull.py` appends a fake Austin, TX temperature reading to `data/events.csv`.
2. `run_model.py` predicts the next reading (average of the last two) and writes
   `output/predict.json`. Each record holds the prediction, the actual value once
   the next reading arrives, and the error (predicted minus actual). The newest
   record has empty `actual` and `error` until the next run fills them in.
3. The results are committed back to the repo.

`index.html` charts the temperature and error for the last 10 predictions. It
fetches `output/predict.json`, so it needs to be served over HTTP. It checks for new
data 30 seconds after each scheduled run, then every minute for half an hour, then
every 5 minutes until the new record shows up (GitHub cron runs are often late), so an
open tab updates on its own. Checks use `If-None-Match` with the server's ETag, so an
unchanged file costs a 304 with no body.

- Locally: `python -m http.server` then open http://localhost:8000/
- On GitHub: enable Pages (Settings → Pages → Deploy from branch → `main`, `/ (root)`).

## Secrets

The workflow passes three repository secrets to the scripts as environment
variables (Settings → Secrets and variables → Actions → New repository secret):

| Secret | Used by | Purpose (demo only, nothing is actually called) |
|---|---|---|
| `VERTICA_USER_NAME` | `db_pull.py` | Vertica login for pulling readings |
| `VERTICA_PASSWORD` | `db_pull.py` | Vertica password |
| `GOOGLE_MAPS_API_KEY` | `run_model.py` | Dallas → Austin drive-time lookup |

If a secret is missing the scripts print a note and continue, so the pipeline
still runs. Secret values are never printed.

Run the workflow manually from the Actions tab ("Run workflow") to get the first data points.
