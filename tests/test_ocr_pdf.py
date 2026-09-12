"""Prova offline del percorso PDF sintetico -> PNG -> API simulata -> testo."""

from __future__ import annotations

import base64
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/ocr-pdf-qwen38-api.py"
SPEC = importlib.util.spec_from_file_location("ocr_pdf_qwen38", SCRIPT)
assert SPEC and SPEC.loader
ocr = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ocr)


def synthetic_pdf(path: Path) -> None:
    """Scrive un PDF testuale minimo senza dipendenze Python esterne."""
    content = b"BT /F1 12 Tf 30 250 Td (Documento sintetico 2042) Tj ET"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n"
        + content + b"\nendstream",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, body in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode() + body + b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n".encode()
    )
    path.write_bytes(output)


class FakeOpener:
    def __init__(self) -> None:
        self.payload = None

    def open(self, request, timeout):
        assert request.full_url == "http://127.0.0.1:8888/v1/chat/completions"
        assert timeout == 1800
        assert request.get_header("Authorization") == "Bearer sk-unsloth-test"
        self.payload = json.loads(request.data)
        answer = {
            "choices": [{"message": {"content": "Documento sintetico 2042"},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 4,
                      "total_tokens": 14},
        }
        return io.BytesIO(json.dumps(answer).encode())


class OcrPdfOfflineTest(unittest.TestCase):
    def test_full_path_uses_synthetic_pdf_and_fake_api(self):
        if not shutil.which("pdfinfo") or not shutil.which("pdftoppm"):
            self.skipTest("Poppler non installato")
        with tempfile.TemporaryDirectory(prefix="ocr-sintetico-") as temp:
            root = Path(temp)
            pdf = root / "esempio-sintetico.pdf"
            output = root / "output"
            synthetic_pdf(pdf)
            fake = FakeOpener()
            args = [str(SCRIPT), str(pdf), "--output", str(output)]
            with patch.object(sys, "argv", args), patch.dict(os.environ, {
                "UNSLOTH_API_KEY": "sk-unsloth-test"
            }), patch.object(ocr.urllib.request, "build_opener", return_value=fake), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(ocr.main(), 0)
            self.assertEqual((output / "page-0001.txt").read_text(),
                             "Documento sintetico 2042\n")
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["source_pdf"], pdf.name)
            self.assertTrue(manifest["results"][0]["complete"])
            self.assertEqual(manifest["results"][0]["total_tokens"], 14)
            parts = fake.payload["messages"][0]["content"]
            uri = parts[1]["image_url"]["url"]
            self.assertTrue(base64.b64decode(uri.split(",", 1)[1]).startswith(
                b"\x89PNG\r\n\x1a\n"
            ))
            self.assertFalse(fake.payload["enable_tools"])

    def test_page_selection_rejects_out_of_range(self):
        self.assertEqual(ocr.selected_pages("3,1-2,2", 3), [1, 2, 3])
        with self.assertRaises(ValueError):
            ocr.selected_pages("0", 3)
        with self.assertRaises(ValueError):
            ocr.selected_pages("4", 3)

    def test_output_inside_repository_is_rejected_before_rendering(self):
        with tempfile.TemporaryDirectory(prefix="ocr-output-") as temp:
            pdf = Path(temp) / "esempio-sintetico.pdf"
            synthetic_pdf(pdf)
            args = [str(SCRIPT), str(pdf), "--output",
                    str(SCRIPT.parents[1] / ".locale" / "out")]
            with patch.object(sys, "argv", args), patch.dict(os.environ, {
                "UNSLOTH_API_KEY": "sk-unsloth-test"
            }), contextlib.redirect_stderr(io.StringIO()), \
                    self.assertRaises(SystemExit):
                ocr.main()


if __name__ == "__main__":
    unittest.main()
