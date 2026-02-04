# Canonical schema definitions for processed MIMIC-IV files

ADMISSIONS_COLUMNS = [
    "subject_id",
    "gender",
    "age",
    "anchor_year",
    "anchor_year_group",
    "subject_id_dup",
    "hadm_id",
    "admit_time",
    "discharge_time",
    "admission_type",
    "admission_location",
    "discharge_location",
    "death_in_hospital",
]

DIAGNOSES_COLUMNS = [
    "subject_id",
    "hadm_id",
    "seq_num",
    "icd_code",
    "icd_version",
]
