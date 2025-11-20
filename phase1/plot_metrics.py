import csv
import matplotlib.pyplot as plt

def plot_metrics():
    t = []
    served = []
    expired = []
    avg_wait = []

    with open("metrics.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t.append(int(row["t"]))
            served.append(int(row["served"]))
            expired.append(int(row["expired"]))
            avg_wait.append(float(row["avg_wait"]))

    plt.figure()
    plt.plot(t, served, label="served")
    plt.plot(t, expired, label="expired")
    plt.plot(t, avg_wait, label="avg_wait")
    plt.xlabel("time")
    plt.ylabel("value")
    plt.legend()
    plt.title("Simulation metrics over time")
    plt.show()

if __name__ == "__main__":
    plot_metrics()
