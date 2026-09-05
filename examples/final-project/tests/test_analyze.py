from pathlib import Path
import sys

sys.path.insert(0, str(Path("/workspace/src")))

from analyze import fit_model, load_table, predicted_at_five


def test_prediction_is_reasonable() -> None:
    table = load_table()
    model = fit_model(table)
    value = predicted_at_five(model)
    assert 40.0 < value < 80.0
