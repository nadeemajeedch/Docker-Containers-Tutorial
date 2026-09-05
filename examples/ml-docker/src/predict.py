from pathlib import Path
import sys

import joblib
import numpy as np


MODEL = Path("/workspace/models/score-model.joblib")


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: python src/predict.py <hours> <practice_sets>")
        sys.exit(1)
    hours = float(sys.argv[1])
    practice = float(sys.argv[2])
    model = joblib.load(MODEL)
    score = float(model.predict(np.array([[hours, practice]]))[0])
    print(f"predicted score: {score:.1f}")


if __name__ == "__main__":
    main()
