from typing import List, Tuple, Set

# Fitness: proportion of observed traces that are covered by the model
def fitness(trace_variants: Set[Tuple[str]], model_traces: Set[Tuple[str]]) -> float:
    if not trace_variants:
        return 0.0
    matched = sum(1 for t in trace_variants if t in model_traces)
    return matched / len(trace_variants)

# Precision: proportion of model traces that match observed behavior
def precision(trace_variants: Set[Tuple[str]], model_traces: Set[Tuple[str]]) -> float:
    if not model_traces:
        return 0.0
    matched = sum(1 for t in model_traces if t in trace_variants)
    return matched / len(model_traces)

# Generalization: ability of the model to allow reasonable unseen behavior
# We define this as 1 - (number of unique variants / number of total traces)
def generalization(trace_variants: Set[Tuple[str]], total_traces: List[Tuple[str]]) -> float:
    if not total_traces:
        return 0.0
    unique_count = len(trace_variants)
    total_count = len(total_traces)
    return 1.0 - (unique_count / total_count)

# Simplicity: penalize models with many distinct activities or transitions
# We define this as 1 - (number of unique activities / max possible transitions)
def simplicity(model_traces: Set[Tuple[str]]) -> float:
    activities = set()
    transitions = set()
    for trace in model_traces:
        activities.update(trace)
        transitions.update(zip(trace[:-1], trace[1:]))
    
    if not transitions:
        return 1.0  # Trivial model

    simplicity_score = 1.0 - (len(activities) / len(transitions))
    return max(0.0, min(1.0, simplicity_score))  # Bound to [0, 1]
