#!/usr/bin/env python3
"""Demo data pull: appends one fake Austin, TX temperature reading to data/events.csv.

Credentials arrive as environment variables set from GitHub Actions secrets
(VERTICA_USER_NAME, VERTICA_PASSWORD). They are read but not used; see connect_db().
"""
import csv
import os
import random
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data") / "events.csv"
FIELDS = ["timestamp", "temp_f"]


def connect_db():
    """Pretend to open a Vertica connection using the supplied credentials.

    In a real pipeline this would be something like:

        import vertica_python
        conn = vertica_python.connect(
            host="vertica.example.com", port=5433, database="weather",
            user=os.environ["VERTICA_USER_NAME"],
            password=os.environ["VERTICA_PASSWORD"],
        )
        cur = conn.cursor()
        cur.execute("SELECT observed_at, temp_f FROM austin_obs ORDER BY observed_at DESC LIMIT 1")

    For this demo we only confirm the secrets were passed in. Values are never printed.
    """
    user = os.environ.get("VERTICA_USER_NAME", "")
    password = os.environ.get("VERTICA_PASSWORD", "")
    if user and password:
        print("Vertica credentials received (demo: no connection is made).")
    else:
        print("Vertica credentials not set; continuing with random data (demo).")
    return None


def last_temp():
    """Return the most recent temperature in the file, or None if there isn't one."""
    if not DATA_FILE.exists():
        return None
    with DATA_FILE.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return float(rows[-1]["temp_f"]) if rows else None


def next_temp(prev):
    """Random walk around a plausible Austin temperature."""
    if prev is None:
        return round(random.uniform(60.0, 95.0), 1)
    return round(max(30.0, min(110.0, prev + random.uniform(-4.0, 4.0))), 1)


def main():
    connect_db()  # demo: would fetch the latest reading from Vertica instead of random data
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    new_file = not DATA_FILE.exists()
    temp = next_temp(last_temp())
    with DATA_FILE.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "temp_f": temp,
        })
    print(f"Appended {temp} F to {DATA_FILE}")


if __name__ == "__main__":
    main()
