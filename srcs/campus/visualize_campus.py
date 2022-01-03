from io import TextIOWrapper

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd


def visualize_campus(csv_file: TextIOWrapper) -> None:
    blackholed = pd.read_csv(csv_file)
    csv_file.close()

    blackholed = blackholed[blackholed["total_user"] > 15].sort_values("percent")

    fig, axes = plt.subplots(1, 2, tight_layout=True)

    y = np.arange(len(blackholed))
    axes[0].barh(y, blackholed["percent"], tick_label=blackholed["campus"])
    axes[0].xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    axes[0].set_title("Percentage of students absorbed into blackhole")

    axes[1].barh(y, blackholed["total_user"], tick_label=blackholed["campus"])
    axes[1].set_title("Number of students")

    plt.show()
