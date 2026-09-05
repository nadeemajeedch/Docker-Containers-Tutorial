import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def main() -> None:
    print("Hello from the Python Docker project")
    print(f"numpy {np.__version__}")
    print(f"pandas {pd.__version__}")

    hours = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(-1, 1)
    scores = np.array([32, 38, 44, 50, 58, 64, 70, 78])
    model = LinearRegression().fit(hours, scores)
    predicted = model.predict(np.array([[5.0]]))[0]

    table = pd.DataFrame({"hours": hours.flatten(), "score": scores})
    print(table.to_string(index=False))
    print(f"predicted score after 5 hours of study: {predicted:.1f}")

    fig, ax = plt.subplots()
    ax.scatter(hours, scores, label="observed")
    ax.plot(hours, model.predict(hours), color="tab:orange", label="fit")
    ax.set_xlabel("hours")
    ax.set_ylabel("score")
    ax.legend()
    fig.savefig("/tmp/study-hours.png", dpi=120)
    print("wrote /tmp/study-hours.png inside the container")


if __name__ == "__main__":
    main()
