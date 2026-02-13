# Example: How to update your notebook cells to use the correct paths

# OLD CODE (Linux path - doesn't work on Windows):
# patients_path = "/data/raw/mimiciv/patients.csv"
# patients_df = pd.read_csv(patients_path, nrows=1000)

# NEW CODE (Windows-compatible with auto-detection):
from data_config import get_data_path

# Method 1: Using the helper function (RECOMMENDED)
patients_path = get_data_path("patients.csv")
patients_df = pd.read_csv(patients_path, nrows=1000)

# Method 2: Direct path (if you know the exact location)
from pathlib import Path
patients_path = Path(r"D:\mimic-iv-3.1\cohort\psy_patients.csv")  # or wherever it is
patients_df = pd.read_csv(patients_path, nrows=1000)

# Method 3: Using the predefined directories
from data_config import COHORT_DIR, UNZIPPED_DIR

admissions_path = COHORT_DIR / "psy_admissions.csv"
admissions_df = pd.read_csv(admissions_path, nrows=1000)

prescriptions_path = UNZIPPED_DIR / "prescriptions.csv"
prescriptions_df = pd.read_csv(prescriptions_path, nrows=1000)
