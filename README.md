# 8INF874 - Project

## Requirements

- Linux-based host
- Python 3.11 (not working on 3.12)

## How to run?

1. (Optional) Create a virtual environment (venv) with `python3 -m venv venv`
   1. (Optional) If a venv was created, activate the venv with `source venv/bin/activate`
2. Install the Python packages with `pip install -r requirements.txt`
3. Generate random files with `sh random_files_generator_linux.sh`. Generated files can be found in `files/`
4. Configure the host, algorithm, key sizesnd file sizes to use in `cryptography.py`
   1. Host (cryptography.py:line 9): add your host name (useful for the reports) and update the index
   2. Algorithm (cryptography.py:line 15): choose the algorithm to use by updating the index
   3. Key sizes (cryptography.py:line 16): update the key sizes list (all key sizes listed will be used)
   4. File sizes (cryptography.py:line 26): update the file sizes list (all file sizes listed will be used)
5. Run the Python script with `python3 cryptography.py`. Reports can be found in `reports/` in the corresponding host name set in 4.1
6. Generate the plots with `python3 report.py`
   1. Host (report.py: line 5): add your host name
   2. RAM (report.py: line 5): add your host RAM amount (can be found from the CodeCarbon output from 5.)
   3. Exclude algorithms (report.py: line 146): exclude outlier algorithms from plot generation
      1. Excluded algorithms will still be generated but won't appear in the "filtered" version
   4. Exclude hosts (report.py: line 147): exclude outlier hosts from plot generation
      1. Excluded hosts will still be generated but won't appear in the "filtered" version