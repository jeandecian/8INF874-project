import matplotlib.pyplot as plt
import pandas as pd
import os

HOST = ("macbook_air_m2", "raspberry_pi_3B", "raspberry_pi_4")
RAM = {"macbook_air_m2": 16, "raspberry_pi_3B": 0.886, "raspberry_pi_4": 7.627}


def read_reports_data():
    data = []

    for host in HOST:
        files = os.listdir(f"reports/{host}")
        csv_files = list(filter(lambda x: x.endswith(".csv"), files))

        for file_name in csv_files:
            file_data = file_name.split("_")
            file_size = file_data[-1].split(".")[0]
            key_size = file_data[-2]
            algorithm = file_data[-3]
            host = "_".join(file_data[1 : len(file_data) - 3])

            temp_df = pd.read_csv(
                f"reports/{host}/emissions_{host}_{algorithm}_{key_size}_{file_size}.csv"
            )

            # See https://mlco2.github.io/codecarbon/output.html for output fields

            temp_df["host"] = host
            temp_df["algorithm"] = algorithm
            temp_df["key_size"] = key_size
            temp_df["file_size"] = file_size
            temp_df["ram"] = RAM[host]
            temp_df["energy_consumed_per_ram"] = (
                temp_df["energy_consumed"] / temp_df["ram"]
            )

            data.append(
                temp_df[
                    [
                        "host",
                        "algorithm",
                        "key_size",
                        "file_size",
                        "ram",
                        "energy_consumed_per_ram",
                        "duration",
                        "emissions",
                        "emissions_rate",
                        "cpu_power",
                        "gpu_power",
                        "ram_power",
                        "cpu_energy",
                        "gpu_energy",
                        "ram_energy",
                        "energy_consumed",
                    ]
                ].iloc[0]
            )

    return data


def convert_to_mb(file_size):
    if "MB" in file_size:
        return float(file_size.replace("MB", ""))
    elif "GB" in file_size:
        return float(file_size.replace("GB", "")) * 1024


def plot_per_host(y, ylabel, title, title_slug, exclude_algorithms=[]):
    for host in HOST:
        for algorithm in algorithms:
            if algorithm not in exclude_algorithms:
                subset = df[
                    (df["host"] == host) & (df["algorithm_key"] == algorithm)
                ].sort_values(by="file_size_MB")

                plt.plot(
                    subset["file_size_MB"],
                    subset[y],
                    marker="+",
                    label=algorithm,
                )

        plt.xlabel("File Size (MB)")
        plt.ylabel(ylabel)

        plt.title(f"{title} by File Size on {host}")
        plt.legend()
        plt.grid(True)

        if len(exclude_algorithms):
            plt.savefig(f"reports/images/{title_slug}_file_size_{host}_filtered.png")
        else:
            plt.savefig(f"reports/images/{title_slug}_file_size_{host}.png")

        plt.show()


UPDATE_DATA = False

data = read_reports_data() if UPDATE_DATA else pd.read_csv("reports/combined.csv")

df = pd.DataFrame(data)

if UPDATE_DATA:
    df.to_csv("reports/combined.csv")

df["algorithm_key"] = df["algorithm"] + "-" + df["key_size"].astype(str)
df["file_size_MB"] = df["file_size"].apply(convert_to_mb)

algorithms = df["algorithm_key"].unique()
exclude_algorithms = ["Twofish-128", "Twofish-192", "Twofish-256", "XTEA-128"]

plt.figure(figsize=(10, 6))

PLOT_PER_HOST = (
    (
        "energy_consumed",
        "Energy Consumed (kWh)",
        "Energy Consumption",
        "energy_consumption",
    ),
    (
        "energy_consumed_per_ram",
        "Energy Consumed Per RAM (kWh/GB)",
        "Energy Consumption Per RAM",
        "energy_consumption_per_ram",
    ),
    ("emissions", "Emissions (kgCO2eq)", "Emissions", "emissions"),
    (
        "emissions_rate",
        "Emissions Rate (kgCO2eq/s)",
        "Emissions Rate",
        "emissions_rate",
    ),
    ("duration", "Duration (s)", "Duration", "duration"),
)


for p in PLOT_PER_HOST:
    plot_per_host(p[0], p[1], p[2], p[3])
    plot_per_host(p[0], p[1], p[2], p[3], exclude_algorithms)
