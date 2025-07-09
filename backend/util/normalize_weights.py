def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weights.values())
    if total > 0:
        normalized_weights = {k: v / total for k, v in weights.items()}
    else:
        raise ValueError("LLM returned no positive weights")

    return normalized_weights