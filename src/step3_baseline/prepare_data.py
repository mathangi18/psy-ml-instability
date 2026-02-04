import pandas as pd

from src.config import (
    ADMISSIONS_FILE,
    DIAGNOSES_FILE,
    PRESCRIPTIONS_FILE,
    METRICS_DIR,
)

from src.schema import (
    ADMISSIONS_COLUMNS,
    DIAGNOSES_COLUMNS,
)


def main():
    # ----------------------------
    # Load admissions with schema
    # ----------------------------
    admissions = pd.read_csv(
        ADMISSIONS_FILE,
        header=None,
        names=ADMISSIONS_COLUMNS,
        parse_dates=["admit_time", "discharge_time"],
    )

    # ----------------------------
    # Load diagnoses with schema
    # ----------------------------
    diagnoses = pd.read_csv(
        DIAGNOSES_FILE,
        header=None,
        names=DIAGNOSES_COLUMNS,
    )

    # ----------------------------
    # Load prescriptions (schema not needed)
    # ----------------------------
    prescriptions = pd.read_csv(
        PRESCRIPTIONS_FILE,
        header=None,
        low_memory=False,
    )

    # ----------------------------
    # Compute length of stay (days)
    # ----------------------------
    admissions["los"] = (
        admissions["discharge_time"] - admissions["admit_time"]
    ).dt.days

    # ----------------------------
    # Diagnosis count per admission
    # ----------------------------
    dx_counts = (
        diagnoses.groupby("hadm_id")
        .size()
        .reset_index(name="diagnosis_count")
    )

    # ----------------------------
    # Medication count per admission
    # ----------------------------
    # hadm_id is column index 1 in prescriptions
    med_counts = (
        prescriptions.groupby(prescriptions.columns[1])
        .size()
        .reset_index(name="medication_count")
        .rename(columns={prescriptions.columns[1]: "hadm_id"})
    )

    # ----------------------------
    # Merge features
    # ----------------------------
    df = admissions.merge(dx_counts, on="hadm_id", how="left")
    df = df.merge(med_counts, on="hadm_id", how="left")

    df["diagnosis_count"] = df["diagnosis_count"].fillna(0)
    df["medication_count"] = df["medication_count"].fillna(0)

    # ----------------------------
    # Targets
    # ----------------------------
    los_median = df["los"].median()
    med_median = df["medication_count"].median()

    df["long_los"] = (df["los"] > los_median).astype(int)
    df["high_med_load"] = (df["medication_count"] > med_median).astype(int)

    # ----------------------------
    # Baseline dataset
    # ----------------------------
    baseline_df = df[
        [
            "hadm_id",
            "age",
            "gender",
            "admission_type",
            "diagnosis_count",
            "medication_count",
            "long_los",
            "high_med_load",
        ]
    ]

    # ----------------------------
    # Save output
    # ----------------------------
    output_path = METRICS_DIR / "baseline_dataset.csv"
    baseline_df.to_csv(output_path, index=False)

    print(f"Baseline dataset saved to {output_path}")
    print(f"Rows: {baseline_df.shape[0]}")


if __name__ == "__main__":
    main()

