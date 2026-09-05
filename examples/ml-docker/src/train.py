from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


DATA = Path("/workspace/data/scores.csv")
MODEL = Path("/workspace/models/score-model.joblib")


def main() -> None:
    table = pd.read_csv(DATA)
    x = table[["hours", "practice_sets"]]
    y = table["score"]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42
    )
    model = LinearRegression().fit(x_train, y_train)
    predicted = model.predict(x_test)
    print(f"n={len(table)}  train={len(x_train)}  test={len(x_test)}")
    print(f"MAE={mean_absolute_error(y_test, predicted):.2f}")
    print(f"R2={r2_score(y_test, predicted):.3f}")
    MODEL.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL)
    print(f"wrote {MODEL}")


if __name__ == "__main__":
    main()
