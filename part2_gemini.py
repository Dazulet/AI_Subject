from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from texts import CORPUS, LANGUAGES

load_dotenv()

MODEL = "gemini-3.5-flash"
OUTPUT_FILE = Path("measurements_gemini_flash.json")


def main():
    client = genai.Client()

    # 1. Count standalone texts
    token_counts = {}

    print(f"MODEL: {MODEL}")
    print("\nTOKEN COUNTS")

    for item_id, versions in CORPUS.items():
        token_counts[item_id] = {}

        print(f"\n{item_id.upper()}")

        for lang in LANGUAGES:
            result = client.models.count_tokens(
                model=MODEL,
                contents=versions[lang],
            )

            count = int(result.total_tokens or 0)
            token_counts[item_id][lang] = count

            print(f"  {lang}: {count}")

    # 2. Complaint ratios
    complaint = token_counts["complaint"]

    ru_ratio = complaint["ru"] / complaint["en"]
    kk_ratio = complaint["kk"] / complaint["en"]

    print("\nCOMPLAINT RATIOS")
    print(f"RU / EN = {ru_ratio:.2f}x")
    print(f"KK / EN = {kk_ratio:.2f}x")

    # 3. Make one real request in each language
    billed = {}

    print("\nREAL REQUESTS")

    for lang in LANGUAGES:
        print(f"\n[{lang.upper()}]")

        response = client.models.generate_content(
            model=MODEL,
            contents=CORPUS["complaint"][lang],
            config=types.GenerateContentConfig(
                system_instruction=CORPUS["system_prompt"][lang],
                max_output_tokens=2048,
            ),
        )

        usage = response.usage_metadata

        input_tokens = int(
            getattr(usage, "prompt_token_count", 0) or 0
        )

        visible_output_tokens = int(
            getattr(usage, "candidates_token_count", 0) or 0
        )

        thinking_tokens = int(
            getattr(usage, "thoughts_token_count", 0) or 0
        )

        total_tokens = int(
            getattr(usage, "total_token_count", 0) or 0
        )

        billable_output_tokens = (
            visible_output_tokens + thinking_tokens
        )

        answer = response.text or ""

        billed[lang] = {
            "input_tokens": input_tokens,
            "visible_output_tokens": visible_output_tokens,
            "thinking_tokens": thinking_tokens,
            "billable_output_tokens": billable_output_tokens,
            "total_tokens": total_tokens,
            "answer": answer,
        }

        print(f"input tokens: {input_tokens}")
        print(f"visible output tokens: {visible_output_tokens}")
        print(f"thinking tokens: {thinking_tokens}")
        print(f"billable output tokens: {billable_output_tokens}")
        print(f"total tokens: {total_tokens}")
        print("\nANSWER:")
        print(answer)

    # 4. Save reproducible results
    data = {
        "provider": "Google Gemini",
        "model": MODEL,
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "token_counts": token_counts,
        "complaint_ratios": {
            "ru_over_en": ru_ratio,
            "kk_over_en": kk_ratio,
        },
        "one_request_billed": billed,
    }

    OUTPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()