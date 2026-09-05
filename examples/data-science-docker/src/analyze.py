from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression


DATA = Path("/workspace/data/study_hours.csv")
RESULTS = Path("/workspace/results")


def load_table() -> pd.DataFrame:
    return pd.read_csv(DATA)


def fit_model(table: pd.DataFrame) -> LinearRegression:
    x = table[["hours"]]
    y = table["score"]
    return LinearRegression().fit(x, y)


def save_plot(table: pd.DataFrame, model: LinearRegression) -> Path:
    RESULTS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots()
    ax.scatter(table["hours"], table["score"], label="observed")
    ax.plot(table["hours"], model.predict(table[["hours"]]), color="tab:orange", label="fit")
    ax.set_xlabel("hours")
    ax.set_ylabel("score")
    ax.legend()
    out = RESULTS / "study-hours.png"
    fig.savefig(out, dpi=120)
    plt.close(fig)
    return out


def main() -> None:
    table = load_table()
    model = fit_model(table)
    predicted = model.predict([[5.0]])[0]
    print(table.to_string(index=False))
    print(f"predicted score after 5 hours: {predicted:.1f}")
    path = save_plot(table, model)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
