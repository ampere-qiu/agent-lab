"""Get the first ten complete HF persona records; no LLM or Groq tokens."""
import hashlib
import io
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
DATASET = "dvilasuero/finepersonas-v0.1-tiny"
BASE = "https://datasets-server.huggingface.co/"
PARAMS = f"dataset={DATASET}&config=default&split=train"
REVISION = "877c402c4434d631b5055853bc50ba93fbdf9c12"
PARQUET_URL = f"https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}/data/train-00000-of-00001.parquet"
PARQUET_SHA256 = "9b5ba66bf5da4f5cdf90385e4b727d586575dce98fd7ada3010876db9bd07d63"


def validate_texts(records):
    if len(records) != 10 or any(not isinstance(text, str) or not text.strip() for text in records):
        raise ValueError("Expected ten complete, non-empty persona descriptions.")
    return records


def request(url):
    return Request(url, headers={"User-Agent": "AgentLab-Week05/1.0"})


def download_rows():
    with urlopen(request(BASE + f"rows?{PARAMS}&offset=0&length=10"), timeout=30) as response:
        rows = json.load(response)["rows"][:10]
    if len(rows) != 10 or [row["row_idx"] for row in rows] != list(range(10)):
        raise ValueError("The rows service did not return rows 0 through 9.")
    if any("persona" in row.get("truncated_cells", []) for row in rows):
        raise ValueError("The rows service truncated persona text.")
    return validate_texts([row["row"]["persona"] for row in rows])


def download_original():
    import pyarrow.parquet as parquet

    print("Using the original dataset file (about 35 MB). Wait for the download; only ten persona texts will be saved.", flush=True)
    deadline = time.monotonic() + 300
    chunks = []
    received = 0
    with urlopen(request(PARQUET_URL + "?download=true"), timeout=30) as response:
        for _ in range(40):
            chunk = response.read(1024 * 1024)
            if time.monotonic() > deadline:
                raise TimeoutError("The original-file download exceeded its time limit.")
            if not chunk:
                break
            chunks.append(chunk)
            received += len(chunk)
            if len(chunks) % 8 == 0:
                print(f"Original file: {received // (1024 * 1024)} MiB received...", flush=True)
    body = b"".join(chunks)
    if hashlib.sha256(body).hexdigest() != PARQUET_SHA256:
        raise ValueError("The original dataset download was incomplete or did not match its checksum.")
    # Read only persona text, not the supplied embeddings or other columns.
    records = parquet.read_table(io.BytesIO(body), columns=["persona"]).column("persona").to_pylist()[:10]
    return validate_texts(records)


def failure_reason(error):
    if isinstance(error, HTTPError):
        return f"the service returned HTTP {error.code}"
    if isinstance(error, (URLError, TimeoutError)):
        return "the connection failed or timed out"
    return str(error).rstrip(".")[:200]


def main():
    target = ROOT / "data"
    if target.exists() and any(target.iterdir()):
        raise SystemExit("data is not empty. Keep your work. If persona_0.txt through persona_9.txt are present, continue to my_ingest.py. Otherwise rename data to data-backup before downloading a fresh set.")
    print("Downloading ten public persona records. Wait for 'Saved 10 persona files' before continuing.", flush=True)
    try:
        records = download_rows()
        source, revision = BASE + f"rows?{PARAMS}&offset=0&length=10", None
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError) as error:
        print("The rows service could not supply complete text: " + failure_reason(error) + ".", flush=True)
        try:
            records = download_original()
            source, revision = PARQUET_URL, REVISION
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, OSError) as backup_error:
            raise SystemExit(
                "The original dataset could not be read: " + failure_reason(backup_error)
                + ". No persona files were written. If a service returned HTTP 503, try later; "
                "that is a server failure, not proof your internet is broken. For a connection error, "
                "check your network. For a checksum failure, retry the download. Keep this message for your instructor."
            ) from None
    target.mkdir(exist_ok=True)
    for number, text in enumerate(records):
        (target / f"persona_{number}.txt").write_text(text, encoding="utf-8")
    (ROOT / "dataset-source.json").write_text(json.dumps({
        "dataset": DATASET, "url": f"https://huggingface.co/datasets/{DATASET}",
        "source": source, "revision": revision, "split": "train", "row_indices": list(range(10)),
    }, indent=2) + "\n", encoding="utf-8")
    print("Saved 10 persona files in data/ (no LLM, no Groq tokens).")


if __name__ == "__main__":
    main()
