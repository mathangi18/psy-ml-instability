# =============================================================================
# MIMIC-IV Data Configuration
# Universal path configuration for raw data access
# =============================================================================

from pathlib import Path
import pandas as pd
import numpy as np

# Set pandas display options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 200)

# ============================================================================
# UNIVERSAL RAW DATA PATH (Windows)
# ============================================================================
RAW_DATA_BASE = Path(r"D:\mimic-iv-3.1")

# Data subdirectories
COHORT_DIR = RAW_DATA_BASE / "cohort"
UNZIPPED_DIR = RAW_DATA_BASE / "Unzipped_raw_data"
STAGED_DIR = RAW_DATA_BASE / "staged"

# ============================================================================
# Helper function to find CSV files
# ============================================================================
def get_data_path(filename):
    """
    Find a CSV file in the MIMIC-IV directory structure.
    
    Args:
        filename: Name of the CSV file (e.g., 'patients.csv', 'admissions.csv')
    
    Returns:
        Path object to the file, or raises FileNotFoundError
    """
    # Check common locations
    search_dirs = [COHORT_DIR, UNZIPPED_DIR, STAGED_DIR, RAW_DATA_BASE]
    
    for directory in search_dirs:
        if directory.exists():
            # Try exact match
            file_path = directory / filename
            if file_path.exists():
                return file_path
            
            # Try with psy_ prefix (for cohort files)
            psy_file_path = directory / f"psy_{filename}"
            if psy_file_path.exists():
                return psy_file_path
    
    # If not found, search recursively
    matches = list(RAW_DATA_BASE.rglob(filename))
    if matches:
        return matches[0]
    
    raise FileNotFoundError(f"Could not find {filename} in {RAW_DATA_BASE}")

# ============================================================================
# Verify data access
# ============================================================================
print("=" * 70)
print("MIMIC-IV Data Configuration")
print("=" * 70)
print(f"Base directory: {RAW_DATA_BASE}")
print(f"Directory exists: {RAW_DATA_BASE.exists()}")
print()

# List available subdirectories
if RAW_DATA_BASE.exists():
    subdirs = [d.name for d in RAW_DATA_BASE.iterdir() if d.is_dir()]
    print(f"Available subdirectories: {', '.join(subdirs)}")
else:
    print("⚠️  WARNING: Base directory not found!")

print("=" * 70)
