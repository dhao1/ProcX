import matplotlib.pyplot as plt

def plot_trace(trace, title='Object Trace'):
    activities = [act for _, act in trace]
    plt.plot(range(len(activities)), activities, marker='o')
    plt.title(title)
    plt.xlabel("Step")
    plt.ylabel("Activity")
    plt.xticks(range(len(activities)))
    plt.grid(True)
    plt.show()
