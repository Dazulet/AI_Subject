import json
from pathlib import Path

REQUESTS_PER_DAY = 5000
REQUESTS_PER_YEAR = REQUESTS_PER_DAY * 365

FILES = {
    "Gemini 3.5 Flash-Lite": Path("measurements_gemini.json"),
    "Gemini 3.5 Flash": Path("measurements_gemini_flash.json"),
}

# USD per 1 million tokens
PRICES = {
    "Gemini 3.5 Flash-Lite": {
        "input": 0.30,
        "output": 2.50,
    },
    "Gemini 3.5 Flash": {
        "input": 1.50,
        "output": 9.00,
    },
}

LANGUAGES = ("en", "ru", "kk")


def request_cost(input_tokens, output_tokens, price):
    return (
        input_tokens * price["input"]
        + output_tokens * price["output"]
    ) / 1_000_000


results = {}

print(
    f"\nVOLUME: {REQUESTS_PER_DAY:,} requests/day "
    f"= {REQUESTS_PER_YEAR:,} requests/year\n"
)

print(
    f"{'MODEL':<26}"
    f"{'LANG':<8}"
    f"{'INPUT':>10}"
    f"{'OUTPUT':>10}"
    f"{'$/REQ':>14}"
    f"{'$/YEAR':>14}"
)

print("-" * 82)

for model_name, file_path in FILES.items():
    data = json.loads(
        file_path.read_text(encoding="utf-8")
    )

    price = PRICES[model_name]
    results[model_name] = {}

    for lang in LANGUAGES:
        usage = data["one_request_billed"][lang]

        input_tokens = usage["input_tokens"]
        output_tokens = usage["billable_output_tokens"]

        per_request = request_cost(
            input_tokens,
            output_tokens,
            price,
        )

        annual = per_request * REQUESTS_PER_YEAR

        results[model_name][lang] = {
            "input_tokens": input_tokens,
            "billable_output_tokens": output_tokens,
            "cost_per_request_usd": per_request,
            "annual_cost_usd": annual,
        }

        print(
            f"{model_name:<26}"
            f"{lang.upper():<8}"
            f"{input_tokens:>10}"
            f"{output_tokens:>10}"
            f"{per_request:>14.6f}"
            f"{annual:>14.2f}"
        )

output = {
    "requests_per_day": REQUESTS_PER_DAY,
    "requests_per_year": REQUESTS_PER_YEAR,
    "results": results,
}

Path("annual_cost.json").write_text(
    json.dumps(output, indent=2),
    encoding="utf-8",
)

print("\nSaved to annual_cost.json")