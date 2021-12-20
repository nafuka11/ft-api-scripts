from io import TextIOWrapper

import matplotlib.pyplot as plt
import pandas as pd


def visualize_correctors(csv_file: TextIOWrapper) -> None:
    correctors = pd.read_csv(csv_file, header=None)
    csv_file.close()

    fig, ax = plt.subplots()
    ax.hist(correctors[1])

    ax.set_xlabel("Number of reviews")
    ax.set_ylabel("Number of reviewers")

    plt.show()
