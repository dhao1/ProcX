def explain_variants(traces):
    variant_counts = {}
    for trace in traces.values():
        variant = tuple([act for _, act in trace])
        variant_counts[variant] = variant_counts.get(variant, 0) + 1
    return sorted(variant_counts.items(), key=lambda x: -x[1])
