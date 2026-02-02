import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

def plot_trajectory_with_drift_twin(time, pred, target, drift, title="Trajectory + Drift (Grok-optimized)"):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(time, pred, label='Predicted', color='blue', linewidth=2)
    ax.plot(time, target, label='Target', color='green', linestyle='--', linewidth=2)
    ax.set_ylabel('Value')
    ax.legend(loc='upper left')

    ax2 = ax.twinx()
    ax2.plot(time, drift, label='Drift (right axis)', color='red', linestyle='solid', linewidth=2)
    ax2.set_ylabel('Drift')
    ax2.legend(loc='upper right', bbox_to_anchor=(1, 1))

    # Grids
    ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.6)
    ax2.grid(True, linestyle='--', color='red', alpha=0.5)  # or 0.4 on dense
    # Optional minor x-grid
    # ax.grid(True, which='minor', axis='x', linestyle=':', color='gray', alpha=0.3)

    plt.title(title)
    plt.tight_layout()
    return fig
