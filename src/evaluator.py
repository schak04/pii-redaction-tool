from typing import List, Tuple, Dict, Any

EntitySpan = Tuple[int, int, str]

class Evaluator:
    @staticmethod
    def evaluate(
        predictions: List[EntitySpan],
        ground_truth: List[EntitySpan],
    ) -> Dict[str, Any]:
        pred_set = set(predictions)
        gt_set = set(ground_truth)

        tp = len(pred_set.intersection(gt_set))
        fp = len(pred_set - gt_set)
        fn = len(gt_set - pred_set)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        return {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
        }
