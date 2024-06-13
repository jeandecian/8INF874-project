import pandas as pd
import os

data = []

for host in ("macbook_air_m2", "raspberry_pi_3B", "raspberry_pi_4"):
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

        temp_df["host"] = host
        temp_df["algorithm"] = algorithm
        temp_df["key_size"] = key_size
        temp_df["file_size"] = file_size

        data.append(
            temp_df[
                [
                    "host",
                    "algorithm",
                    "key_size",
                    "file_size",
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

df = pd.DataFrame(data)

print(df)
