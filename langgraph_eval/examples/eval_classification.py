from dataclasses import dataclass

@dataclass
class Metrics:
    accuracy: float
    precision: float
    recall: float
    f1: float

def evaluate(y_true: list[int], y_pred: list[int]) -> Metrics:
    tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
    tn = sum(t == 0 and p == 0 for t, p in zip(y_true, y_pred))
    fp = sum(t == 0 and p == 1 for t, p in zip(y_true, y_pred))
    fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))

    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return Metrics(accuracy, precision, recall, f1)

if __name__ == "__main__":
    print(evaluate([1, 1, 0, 0], [1, 0, 0, 0]))
