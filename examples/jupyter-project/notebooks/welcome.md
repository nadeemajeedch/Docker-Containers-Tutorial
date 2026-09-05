# Welcome notebook (markdown starter)

This folder is bind-mounted into the Jupyter container as `/home/jovyan/work`.

Create a notebook in JupyterLab named `01-check-stack.ipynb` and run:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

print("numpy", np.__version__)
print("pandas", pd.__version__)
print("sklearn", sklearn.__version__)

x = np.linspace(0, 2 * np.pi, 50)
plt.plot(x, np.sin(x))
plt.title("sin(x) from the custom Jupyter image")
plt.show()
```

Save the notebook. Because of the bind mount, the `.ipynb` file appears on your host under `examples/jupyter-project/notebooks/`.

A sample notebook JSON file is included as `01-check-stack.ipynb`.
