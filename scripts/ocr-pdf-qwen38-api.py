#!/usr/bin/env python3
"""OCR locale di PDF tramite Qwen Vision e API OpenAI-compatible di Studio.

Renderizza e invia una pagina per richiesta. Scrive soltanto nella cartella di
output scelta: testo per pagina e manifest JSON. Non altera il PDF originale.
Input e output devono stare fuori da questo repository. Richiede una chiave
API ufficiale di Unsloth in UNSLOTH_API_KEY.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


BASE = "http://127.0.0.1:8888"
MODEL = "unsloth/Qwen3.8-27B-GGUF"
ROOT = Path(__file__).resolve().parents[1]
PROMPT = (
    "Trascrivi fedelmente tutto il testo visibile in questa pagina, "
    "nell'ordine di lettura. Conserva numeri, sigle, date, importi e "
    "punteggiatura. Se un tratto non è leggibile, scrivi [illeggibile]. "
    "Non completare parole per supposizione e non commentare il contenuto."
)


def count_pages(pdf: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(pdf)], capture_output=True, text=True, check=True
    )
    match = re.search(r"^Pages:\s*(\d+)\s*$", result.stdout, re.MULTILINE)
    if not match:
        raise ValueError("pdfinfo non ha restituito il numero di pagine")
    return int(match.group(1))


def selected_pages(spec: str | None, total: int) -> list[int]:
    if not spec:
        return list(range(1, total + 1))
    selected: set[int] = set()
    for part in spec.split(","):
        bits = part.strip().split("-", 1)
        if not all(x.isdecimal() for x in bits):
            raise ValueError("--pages richiede numeri o intervalli, es. 1,3-5")
        first, last = int(bits[0]), int(bits[-1])
        if first < 1 or last > total or first > last:
            raise ValueError(f"pagina fuori intervallo 1-{total}")
        selected.update(range(first, last + 1))
    return sorted(selected)


def render_page(pdf: Path, page: int, dpi: int, directory: Path) -> bytes:
    prefix = directory / f"page-{page:04d}"
    subprocess.run(
        ["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi),
         "-singlefile", "-png", str(pdf), str(prefix)],
        capture_output=True, check=True,
    )
    return prefix.with_suffix(".png").read_bytes()


def content_text(value: object) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(
            block["text"] for block in value
            if isinstance(block, dict) and block.get("type") == "text"
            and isinstance(block.get("text"), str)
        ).strip()
    return ""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ocr_page(opener, key: str, png: bytes, max_tokens: int) -> tuple[str, dict]:
    uri = "data:image/png;base64," + base64.b64encode(png).decode("ascii")
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url", "image_url": {"url": uri}},
        ]}],
        "temperature": 0,
        "max_tokens": max_tokens,
        "enable_thinking": False,
        "enable_tools": False,
        "stream": False,
    }
    request = urllib.request.Request(
        BASE + "/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json"},
        method="POST",
    )
    with opener.open(request, timeout=1800) as response:
        data = json.load(response)
    choice = data.get("choices", [{}])[0]
    text = content_text(choice.get("message", {}).get("content"))
    usage = data.get("usage", {})
    metadata = {
        "finish_reason": choice.get("finish_reason"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "complete": bool(text) and choice.get("finish_reason") == "stop",
    }
    return text, metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--pages", help="Pagine 1-based, es. 1,3-5; default: tutte")
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--max-tokens", type=int, default=4096)
    args = parser.parse_args()
    key = os.environ.get("UNSLOTH_API_KEY", "")
    if not key.startswith("sk-unsloth-"):
        parser.error("serve una chiave API ufficiale in UNSLOTH_API_KEY")
    pdf = args.pdf.resolve(strict=True)
    if pdf.suffix.lower() != ".pdf":
        parser.error("il file in ingresso deve essere un PDF")
    if not 72 <= args.dpi <= 400 or not 128 <= args.max_tokens <= 8192:
        parser.error("dpi deve essere 72-400 e max-tokens 128-8192")
    output = args.output.resolve()
    if output == pdf.parent or output == pdf:
        parser.error("scegliere una cartella di output dedicata")
    if pdf.is_relative_to(ROOT) or output.is_relative_to(ROOT):
        parser.error("input e output devono stare fuori da questo repository")
    if output.exists() and not output.is_dir():
        parser.error("il percorso di output esiste e non è una cartella")
    if output.exists() and any(output.iterdir()):
        parser.error("la cartella di output deve essere nuova o vuota; nessun file verrà sovrascritto")
    total = count_pages(pdf)
    pages = selected_pages(args.pages, total)
    output.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    manifest = {
        "schema": 1,
        "source_pdf": pdf.name,
        "source_sha256": sha256_file(pdf),
        "model": MODEL,
        "dpi": args.dpi,
        "page_count": total,
        "selected_pages": pages,
        "results": [],
    }
    for page in pages:
        try:
            with tempfile.TemporaryDirectory(prefix="qwen-ocr-") as temp:
                png = render_page(pdf, page, args.dpi, Path(temp))
                text, metadata = ocr_page(opener, key, png, args.max_tokens)
        except (subprocess.CalledProcessError, urllib.error.HTTPError,
                urllib.error.URLError, TimeoutError, ValueError) as exc:
            # Non stampare body HTTP o testo PDF: possono contenere dati riservati.
            status = getattr(exc, "code", None)
            print(f"Pagina {page}: errore di rendering/API (HTTP {status or 'n/d'}).")
            return 1
        filename = f"page-{page:04d}.txt"
        (output / filename).write_text(text + "\n", encoding="utf-8")
        manifest["results"].append({"page": page, "file": filename, **metadata})
        (output / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Pagina {page}/{total}: {'completa' if metadata['complete'] else 'da verificare'}, "
              f"token totali {metadata['total_tokens'] if metadata['total_tokens'] is not None else 'n/d'}.")
    return 0 if all(row["complete"] for row in manifest["results"]) else 2


if __name__ == "__main__":
    raise SystemExit(main())
