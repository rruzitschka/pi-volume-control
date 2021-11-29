#this module creates a graph of the volume values

import numpy as np
import math
import matplotlib.pyplot as plt


def plot_volume(volume):
    plt.plot(volume)
    plt.savefig('volume_graph.png')