from typing import Dict

def suggest_price(watch: Dict) -> float:
    # Mock market data
    mock_market_data = {
        "similarWatches": [
            {"brand": watch["brand"], "model": watch["model"], "price": 5000, "condition": "excellent"},
            {"brand": watch["brand"], "model": watch["model"], "price": 4500, "condition": "good"},
            {"brand": watch["brand"], "model": watch["model"], "price": 4000, "condition": "fair"}
        ]
    }

    average_price = sum(item["price"] for item in mock_market_data["similarWatches"]) / len(mock_market_data["similarWatches"])
    condition_multiplier = {"excellent": 1.2, "good": 1.0, "fair": 0.8}.get(watch["condition"], 1.0)
    return average_price * condition_multiplier