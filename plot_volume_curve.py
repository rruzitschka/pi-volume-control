import numpy as np
import math
import matplotlib.pyplot as plt


def plot_volume(volume):
    plt.plot(volume)
    plt.savefig('foo.png')
    plt.show(block=True)