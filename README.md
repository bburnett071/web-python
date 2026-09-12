# Austin temperature demo pipeline

Demo only. A GitHub Action runs every 4 hours and:

1. `db_pull.py` appends a fake Austin, TX temperature reading to `data/events.csv`.
2. `run_model.py` predicts the next reading (average of the last two) and writes
   `output/predict.json`. Each record holds the prediction, the actual value once
   the next reading arrives, and the error (predicted minus actual). The newest
   record has empty `actual` and `error` until the next run fills them in.
3. The results are committed back to the repo.

`index.html` charts the temperature and error for the last 10 predictions. It
fetches `output/predict.json`, so it needs to be served over HTTP. It re-fetches
the data 30 seconds after each scheduled run (every 4 hours, UTC) and keeps checking
each minute until the new record appears, so an open tab updates on its own.

- Locally: `python -m http.server` then open http://localhost:8000/
- On GitHub: enable Pages (Settings → Pages → Deploy from branch → `main`, `/ (root)`).

Run the workflow manually from the Actions tab ("Run workflow") to get the first data points.
