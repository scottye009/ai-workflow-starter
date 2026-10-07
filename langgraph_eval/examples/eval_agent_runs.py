from dataclasses import dataclass

@dataclass
class RunResult:
    success: bool
    escalated: bool
    steps: int
    latency_ms: float
    cost_usd: float

def summarize(runs: list[RunResult]) -> dict:
    if not runs:
        raise ValueError("runs cannot be empty")

    n = len(runs)
    return {
        "task_success_rate": sum(r.success for r in runs) / n,
        "escalation_rate": sum(r.escalated for r in runs) / n,
        "avg_steps": sum(r.steps for r in runs) / n,
        "avg_latency_ms": sum(r.latency_ms for r in runs) / n,
        "avg_cost_usd": sum(r.cost_usd for r in runs) / n,
    }

if __name__ == "__main__":
    runs = [
        RunResult(True, False, 3, 1200, 0.03),
        RunResult(True, True, 4, 1800, 0.04),
        RunResult(False, True, 6, 2600, 0.06),
    ]
    print(summarize(runs))
