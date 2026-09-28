import pandas as pd
import random
from datetime import date, timedelta

# Make results reproducible
random.seed(2026)

# Study settings
NUM_SUBJECTS = 500
STUDY_ID = "ONC-2026-001"

# Study sites
sites = [f"{i:02d}" for i in range(1, 11)]

# Treatment arms
treatments = [
    "ABC-101 50 mg",
    "ABC-101 100 mg",
    "Placebo"
]

# Demographic choices
sexes = [
    "Male",
    "Female",
    "Other",
    "Not Reported"
]

races = [
    "American Indian or Alaska Native",
    "Asian",
    "Black or African American",
    "Native Hawaiian or Other Pacific Islander",
    "White",
    "Multiple Races",
    "Not Reported"
]

ethnicities = [
    "Hispanic or Latino",
    "Not Hispanic or Latino",
    "Not Reported"
]

# Screening outcomes
screening_statuses = [
    "Eligible",
    "Not Eligible",
    "Pending"
]

# Store generated subjects
subjects = []

# Generate 500 subjects
for i in range(1, NUM_SUBJECTS + 1):

    # Subject ID
    subject_id = f"ONC-{i:04d}"

    # Random study site
    site_id = random.choice(sites)

    # Random consent date during the study enrollment period
    consent_date = date(2026, 1, 1) + timedelta(
        days=random.randint(0, 180)
    )

    # Random date of birth
    birth_year = random.randint(1950, 2000)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)

    date_of_birth = date(
        birth_year,
        birth_month,
        birth_day
    )

    # Calculate age at consent
    age = consent_date.year - date_of_birth.year

    if (consent_date.month, consent_date.day) < (
        date_of_birth.month,
        date_of_birth.day
    ):
        age -= 1

    # Demographics
    sex = random.choice(sexes)
    race = random.choice(races)
    ethnicity = random.choice(ethnicities)

    # Height and weight
    height_cm = round(random.uniform(150, 195), 1)
    weight_kg = round(random.uniform(50, 120), 1)

    # Treatment assignment
    treatment = random.choice(treatments)

    # Screening status
    screening_status = random.choices(
        screening_statuses,
        weights=[0.90, 0.08, 0.02]
    )[0]

    # Screening failure reason
    screen_fail_reason = ""

    if screening_status == "Not Eligible":
        screen_fail_reason = random.choice([
            "Did not meet inclusion criteria",
            "Did not meet laboratory eligibility criteria",
            "Eligibility criteria not satisfied"
        ])

    # Add subject record
    subjects.append({
        "study_id": STUDY_ID,
        "subject_id": subject_id,
        "site_id": site_id,
        "consent_date": consent_date,
        "date_of_birth": date_of_birth,
        "age": age,
        "sex": sex,
        "race": race,
        "ethnicity": ethnicity,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "treatment": treatment,
        "screening_status": screening_status,
        "screen_fail_reason": screen_fail_reason
    })


# Create DataFrame
subjects_df = pd.DataFrame(subjects)


# Format dates as YYYY-MM-DD
subjects_df["consent_date"] = pd.to_datetime(
    subjects_df["consent_date"]
).dt.strftime("%Y-%m-%d")

subjects_df["date_of_birth"] = pd.to_datetime(
    subjects_df["date_of_birth"]
).dt.strftime("%Y-%m-%d")


# Save the synthetic subject dataset
output_file = "../03_Raw data/subjects_raw.csv"

subjects_df.to_csv(
    output_file,
    index=False
)


# Display confirmation
print()
print("=" * 50)
print("SYNTHETIC SUBJECT DATA GENERATED")
print("=" * 50)
print(f"Study ID: {STUDY_ID}")
print(f"Number of subjects: {len(subjects_df)}")
print(f"Output file: {output_file}")
print()
print("First 5 records:")
print(subjects_df.head())
print()
print("Treatment distribution:")
print(subjects_df["treatment"].value_counts())
print()
print("Screening status distribution:")
print(subjects_df["screening_status"].value_counts())
print("=" * 50)


# ============================================================
# GENERATE MEDICAL HISTORY DATA
# ============================================================

medical_conditions = [
    ("Type 2 Diabetes", "Endocrine/Metabolic"),
    ("Hypertension", "Cardiovascular"),
    ("Hyperlipidemia", "Endocrine/Metabolic"),
    ("Asthma", "Respiratory"),
    ("Chronic Kidney Disease", "Renal"),
    ("Gastroesophageal Reflux Disease", "Gastrointestinal"),
    ("Migraine", "Neurological"),
    ("Osteoarthritis", "Other")
]

medical_history = []

for _, subject in subjects_df.iterrows():

    # Each subject has 1 to 3 medical history records
    num_conditions = random.randint(1, 3)

    selected_conditions = random.sample(
        medical_conditions,
        num_conditions
    )

    for condition, category in selected_conditions:

        # Condition started before study consent
        start_date = pd.to_datetime(
            subject["consent_date"]
        ).date() - timedelta(
            days=random.randint(365, 2500)
        )

        # Most conditions are ongoing
        ongoing = random.choices(
            ["Yes", "No"],
            weights=[0.70, 0.30]
        )[0]

        end_date = ""

        if ongoing == "No":
            end_date = start_date + timedelta(
                days=random.randint(180, 1500)
            )

            # Make sure the condition ended before consent
            consent_date = pd.to_datetime(
                subject["consent_date"]
            ).date()

            if end_date >= consent_date:
                end_date = consent_date - timedelta(days=30)

        medical_history.append({
            "subject_id": subject["subject_id"],
            "medical_condition": condition,
            "condition_category": category,
            "condition_start_date": start_date,
            "condition_end_date": end_date,
            "condition_ongoing": ongoing,
            "medical_history_comments": ""
        })


# Create DataFrame
medical_history_df = pd.DataFrame(medical_history)


# Format dates
medical_history_df["condition_start_date"] = pd.to_datetime(
    medical_history_df["condition_start_date"]
).dt.strftime("%Y-%m-%d")

medical_history_df["condition_end_date"] = pd.to_datetime(
    medical_history_df["condition_end_date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

medical_history_df["condition_end_date"] = (
    medical_history_df["condition_end_date"]
    .fillna("")
)


# Save Medical History dataset
medical_history_output = "../03_Raw data/medical_history_raw.csv"

medical_history_df.to_csv(
    medical_history_output,
    index=False
)


# Display confirmation
print()
print("=" * 50)
print("MEDICAL HISTORY DATA GENERATED")
print("=" * 50)
print(f"Number of medical history records: {len(medical_history_df)}")
print(f"Output file: {medical_history_output}")
print()
print("First 5 records:")
print(medical_history_df.head())
print()
print("Conditions by category:")
print(
    medical_history_df["condition_category"].value_counts()
)
print("=" * 50)



# ============================================================
# GENERATE STUDY VISIT DATA
# ============================================================

visit_schedule = [
    ("Screening", -14, 0),
    ("Baseline", 1, 0),
    ("Week 2", 14, 3),
    ("Week 4", 28, 5),
    ("Week 8", 56, 7),
    ("Week 12", 84, 7),
    ("End of Study", 90, 7)
]

visits = []

for _, subject in subjects_df.iterrows():

    consent_date = pd.to_datetime(
        subject["consent_date"]
    ).date()

    treatment = subject["treatment"]

    screening_status = subject["screening_status"]

    # Subjects who fail screening do not continue to later visits
    if screening_status == "Not Eligible":

        visit_name, target_day, window = visit_schedule[0]

        visit_date = consent_date

        visits.append({
            "subject_id": subject["subject_id"],
            "visit_name": visit_name,
            "visit_date": visit_date,
            "visit_status": "Completed",
            "treatment_assignment": treatment,
            "visit_completed": "Yes",
            "visit_not_completed_reason": "",
            "visit_comments": ""
        })

        continue

    # Pending subjects only have screening for now
    if screening_status == "Pending":

        visit_name, target_day, window = visit_schedule[0]

        visit_date = consent_date

        visits.append({
            "subject_id": subject["subject_id"],
            "visit_name": visit_name,
            "visit_date": visit_date,
            "visit_status": "Completed",
            "treatment_assignment": treatment,
            "visit_completed": "Yes",
            "visit_not_completed_reason": "",
            "visit_comments": ""
        })

        continue

    # Eligible subjects receive the full visit schedule
    for visit_name, target_day, window in visit_schedule:

        # Screening occurs on consent date
        if visit_name == "Screening":
            visit_date = consent_date

        else:
            target_date = consent_date + timedelta(days=target_day)

            # Generate a date within the protocol visit window
            if window > 0:
                day_offset = random.randint(-window, window)
            else:
                day_offset = 0

            visit_date = target_date + timedelta(days=day_offset)

        # Small percentage of scheduled visits are missed
        if visit_name not in ["Screening", "Baseline"]:
            missed = random.random() < 0.04
        else:
            missed = False

        if missed:

            visit_status = "Missed"
            visit_completed = "No"

            visit_not_completed_reason = random.choice([
                "Subject unavailable",
                "Subject withdrew before visit",
                "Scheduling conflict",
                "Missed appointment"
            ])

        else:

            visit_status = "Completed"
            visit_completed = "Yes"
            visit_not_completed_reason = ""

        visits.append({
            "subject_id": subject["subject_id"],
            "visit_name": visit_name,
            "visit_date": visit_date,
            "visit_status": visit_status,
            "treatment_assignment": treatment,
            "visit_completed": visit_completed,
            "visit_not_completed_reason": visit_not_completed_reason,
            "visit_comments": ""
        })


# Create DataFrame
visits_df = pd.DataFrame(visits)


# Format visit date
visits_df["visit_date"] = pd.to_datetime(
    visits_df["visit_date"]
).dt.strftime("%Y-%m-%d")


# Save Study Visit dataset
visits_output = "../03_Raw data/visits_raw.csv"

visits_df.to_csv(
    visits_output,
    index=False
)


# Display confirmation
print()
print("=" * 50)
print("STUDY VISIT DATA GENERATED")
print("=" * 50)
print(f"Number of visit records: {len(visits_df)}")
print(f"Output file: {visits_output}")
print()
print("Visit distribution:")
print(visits_df["visit_name"].value_counts())
print()
print("Visit status distribution:")
print(visits_df["visit_status"].value_counts())
print("=" * 50)

# ============================================================
# GENERATE VITAL SIGNS DATA
# ============================================================

vital_signs = []

for _, visit in visits_df.iterrows():

    # Only collect vital signs for completed visits
    if visit["visit_status"] != "Completed":
        continue

    subject_id = visit["subject_id"]
    visit_name = visit["visit_name"]
    visit_date = visit["visit_date"]

    # Find subject's baseline weight
    subject_row = subjects_df[
        subjects_df["subject_id"] == subject_id
    ].iloc[0]

    baseline_weight = subject_row["weight_kg"]

    # Small realistic weight change over time
    weight_change = random.uniform(-3, 3)

    weight = round(
        float(baseline_weight) + weight_change,
        1
    )

    # Generate vital signs
    systolic_bp = random.randint(105, 150)

    diastolic_bp = random.randint(65, 95)

    heart_rate = random.randint(55, 95)

    respiratory_rate = random.randint(12, 20)

    temperature_c = round(
        random.uniform(36.1, 37.4),
        1
    )

    vital_signs.append({
        "subject_id": subject_id,
        "visit_name": visit_name,
        "visit_date": visit_date,
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
        "heart_rate": heart_rate,
        "respiratory_rate": respiratory_rate,
        "temperature_c": temperature_c,
        "weight_kg": weight,
        "comments": ""
    })


# Create DataFrame
vital_signs_df = pd.DataFrame(vital_signs)


# Save Vital Signs dataset
vital_signs_output = "../03_Raw data/vital_signs_raw.csv"

vital_signs_df.to_csv(
    vital_signs_output,
    index=False
)


# Display confirmation
print()
print("=" * 50)
print("VITAL SIGNS DATA GENERATED")
print("=" * 50)
print(f"Number of vital sign records: {len(vital_signs_df)}")
print(f"Output file: {vital_signs_output}")
print()
print("First 5 records:")
print(vital_signs_df.head())
print()
print("Vital sign columns:")
print(list(vital_signs_df.columns))
print("=" * 50)


# ============================================================
# GENERATE LABORATORY DATA
# ============================================================

lab_tests = {
    "HbA1c": {
        "unit": "%",
        "low": 4.0,
        "high": 5.6
    },
    "Glucose": {
        "unit": "mg/dL",
        "low": 70,
        "high": 99
    },
    "Creatinine": {
        "unit": "mg/dL",
        "low": 0.6,
        "high": 1.3
    },
    "ALT": {
        "unit": "U/L",
        "low": 7,
        "high": 56
    },
    "AST": {
        "unit": "U/L",
        "low": 10,
        "high": 40
    },
    "Hemoglobin": {
        "unit": "g/dL",
        "low": 12.0,
        "high": 17.5
    }
}

laboratory = []

for _, visit in visits_df.iterrows():

    # Only collect laboratory data for completed visits
    if visit["visit_status"] != "Completed":
        continue

    subject_id = visit["subject_id"]
    visit_name = visit["visit_name"]
    visit_date = visit["visit_date"]

    # Generate all six laboratory tests
    for test_name, test_info in lab_tests.items():

        low = test_info["low"]
        high = test_info["high"]
        unit = test_info["unit"]

        # Generate values around the reference range
        if test_name == "HbA1c":
            result = round(random.uniform(5.5, 9.5), 1)

        elif test_name == "Glucose":
            result = round(random.uniform(75, 180), 0)

        elif test_name == "Creatinine":
            result = round(random.uniform(0.6, 1.4), 2)

        elif test_name == "ALT":
            result = round(random.uniform(10, 80), 1)

        elif test_name == "AST":
            result = round(random.uniform(12, 65), 1)

        elif test_name == "Hemoglobin":
            result = round(random.uniform(11.0, 17.0), 1)

        # Determine abnormal flag
        if result > high:
            abnormal_flag = "High"

        elif result < low:
            abnormal_flag = "Low"

        else:
            abnormal_flag = "Normal"

        laboratory.append({
            "subject_id": subject_id,
            "visit_name": visit_name,
            "lab_collection_date": visit_date,
            "lab_test": test_name,
            "lab_result": result,
            "lab_unit": unit,
            "reference_low": low,
            "reference_high": high,
            "abnormal_flag": abnormal_flag,
            "lab_comments": ""
        })


# Create DataFrame
laboratory_df = pd.DataFrame(laboratory)


# Save Laboratory dataset
laboratory_output = "../03_Raw data/laboratory_raw.csv"

laboratory_df.to_csv(
    laboratory_output,
    index=False
)


# Display confirmation
print()
print("=" * 50)
print("LABORATORY DATA GENERATED")
print("=" * 50)
print(f"Number of laboratory records: {len(laboratory_df)}")
print(f"Output file: {laboratory_output}")
print()
print("Laboratory test distribution:")
print(
    laboratory_df["lab_test"].value_counts()
)
print()
print("Abnormal flag distribution:")
print(
    laboratory_df["abnormal_flag"].value_counts()
)
print("=" * 50)



# ============================================================
# GENERATE ADVERSE EVENTS DATA
# ============================================================

ae_terms = [
    "Headache",
    "Nausea",
    "Dizziness",
    "Fatigue",
    "Diarrhea",
    "Injection Site Reaction",
    "Upper Respiratory Tract Infection",
    "Hypoglycemia",
    "Abdominal Pain"
]

ae_severities = [
    "Mild",
    "Moderate",
    "Severe"
]

ae_relationships = [
    "Not Related",
    "Unlikely Related",
    "Possibly Related",
    "Probably Related",
    "Definitely Related"
]

ae_actions = [
    "None",
    "Dose Not Changed",
    "Dose Reduced",
    "Drug Interrupted",
    "Drug Withdrawn",
    "Other"
]

ae_outcomes = [
    "Recovered/Resolved",
    "Recovering/Resolving",
    "Not Recovered/Not Resolved",
    "Recovered With Sequelae",
    "Unknown"
]

adverse_events = []

# Approximately 25% of subjects will have at least one AE
for _, subject in subjects_df.iterrows():

    if random.random() > 0.25:
        continue

    subject_id = subject["subject_id"]

    consent_date = pd.to_datetime(
        subject["consent_date"]
    ).date()

    # Generate 1–2 AEs
    num_aes = random.choices(
        [1, 2],
        weights=[0.85, 0.15]
    )[0]

    for _ in range(num_aes):

        ae_term = random.choice(ae_terms)

        # AE starts after consent
        ae_start_date = consent_date + timedelta(
            days=random.randint(5, 100)
        )

        # Most AEs are not ongoing
        ongoing = random.choices(
            ["Yes", "No"],
            weights=[0.20, 0.80]
        )[0]

        ae_end_date = ""

        if ongoing == "No":
            duration = random.randint(1, 14)

            ae_end_date = ae_start_date + timedelta(
                days=duration
            )

        seriousness = random.choices(
            ["Serious", "Non-Serious"],
            weights=[0.05, 0.95]
        )[0]

        severity = random.choices(
            ae_severities,
            weights=[0.65, 0.30, 0.05]
        )[0]

        relationship = random.choices(
            ae_relationships,
            weights=[0.30, 0.20, 0.35, 0.10, 0.05]
        )[0]

        action = random.choices(
            ae_actions,
            weights=[0.60, 0.20, 0.08, 0.05, 0.03, 0.04]
        )[0]

        # Fatal outcome is intentionally excluded from
        # the normal synthetic dataset
        if ongoing == "Yes":
            outcome = "Recovering/Resolving"
        else:
            outcome = random.choice([
                "Recovered/Resolved",
                "Recovered/Resolved",
                "Recovered/Resolved",
                "Unknown"
            ])

        adverse_events.append({
            "subject_id": subject_id,
            "visit_name": "",
            "ae_term": ae_term,
            "ae_start_date": ae_start_date,
            "ae_end_date": ae_end_date,
            "ae_ongoing": ongoing,
            "ae_seriousness": seriousness,
            "ae_severity": severity,
            "ae_relationship": relationship,
            "ae_action": action,
            "ae_outcome": outcome,
            "ae_comments": ""
        })


# Create DataFrame
adverse_events_df = pd.DataFrame(adverse_events)


# Format dates
adverse_events_df["ae_start_date"] = pd.to_datetime(
    adverse_events_df["ae_start_date"]
).dt.strftime("%Y-%m-%d")

adverse_events_df["ae_end_date"] = pd.to_datetime(
    adverse_events_df["ae_end_date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

adverse_events_df["ae_end_date"] = (
    adverse_events_df["ae_end_date"]
    .fillna("")
)


# Save Adverse Events dataset
ae_output = "../03_Raw data/adverse_events_raw.csv"

adverse_events_df.to_csv(
    ae_output,
    index=False
)


# Display confirmation
print()
print("=" * 50)
print("ADVERSE EVENTS DATA GENERATED")
print("=" * 50)
print(f"Number of AE records: {len(adverse_events_df)}")
print(f"Output file: {ae_output}")
print()

if len(adverse_events_df) > 0:

    print("AE term distribution:")
    print(
        adverse_events_df["ae_term"].value_counts()
    )

    print()
    print("Severity distribution:")
    print(
        adverse_events_df["ae_severity"].value_counts()
    )

    print()
    print("Seriousness distribution:")
    print(
        adverse_events_df["ae_seriousness"].value_counts()
    )

print("=" * 50)


# ============================================================
# GENERATE CONCOMITANT MEDICATIONS DATA
# ============================================================

medications = [
    ("Metformin", "Type 2 Diabetes", "500 mg twice daily"),
    ("Lisinopril", "Hypertension", "10 mg once daily"),
    ("Atorvastatin", "Hyperlipidemia", "20 mg once daily"),
    ("Aspirin", "Cardiovascular prevention", "81 mg once daily"),
    ("Omeprazole", "Gastroesophageal reflux", "20 mg once daily"),
    ("Albuterol", "Asthma", "2 puffs as needed"),
    ("Ibuprofen", "Pain", "200 mg as needed"),
    ("Acetaminophen", "Pain", "500 mg as needed")
]

concomitant_medications = []

for _, subject in subjects_df.iterrows():

    subject_id = subject["subject_id"]

    consent_date = pd.to_datetime(
        subject["consent_date"]
    ).date()

    # Approximately 70% of subjects have at least one
    # concomitant medication
    if random.random() > 0.70:
        continue

    # Each subject receives 1–3 medications
    num_medications = random.randint(1, 3)

    selected_medications = random.sample(
        medications,
        num_medications
    )

    for medication_name, indication, dose_frequency in selected_medications:

        # Medication starts before or during the study
        start_offset = random.randint(30, 2000)

        medication_start_date = (
            consent_date - timedelta(days=start_offset)
        )

        # Most medications are ongoing
        ongoing = random.choices(
            ["Yes", "No"],
            weights=[0.75, 0.25]
        )[0]

        medication_end_date = ""

        if ongoing == "No":

            medication_end_date = (
                medication_start_date
                + timedelta(days=random.randint(30, 1000))
            )

            # Ensure medication ended before consent
            if medication_end_date >= consent_date:
                medication_end_date = (
                    consent_date - timedelta(days=random.randint(1, 30))
                )

        concomitant_medications.append({
            "subject_id": subject_id,
            "medication_name": medication_name,
            "medication_indication": indication,
            "medication_start_date": medication_start_date,
            "medication_end_date": medication_end_date,
            "medication_ongoing": ongoing,
            "medication_dose_frequency": dose_frequency,
            "cm_comments": ""
        })


# Create DataFrame
concomitant_medications_df = pd.DataFrame(
    concomitant_medications
)


# Format dates
concomitant_medications_df[
    "medication_start_date"
] = pd.to_datetime(
    concomitant_medications_df[
        "medication_start_date"
    ]
).dt.strftime("%Y-%m-%d")

concomitant_medications_df[
    "medication_end_date"
] = pd.to_datetime(
    concomitant_medications_df[
        "medication_end_date"
    ],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

concomitant_medications_df[
    "medication_end_date"
] = (
    concomitant_medications_df[
        "medication_end_date"
    ].fillna("")
)


# Save Concomitant Medications dataset
cm_output = "../03_Raw data/concomitant_medications_raw.csv"

concomitant_medications_df.to_csv(
    cm_output,
    index=False
)


# Display confirmation
print()
print("=" * 50)
print("CONCOMITANT MEDICATIONS DATA GENERATED")
print("=" * 50)
print(
    f"Number of medication records: "
    f"{len(concomitant_medications_df)}"
)
print(f"Output file: {cm_output}")
print()

if len(concomitant_medications_df) > 0:

    print("Medication distribution:")
    print(
        concomitant_medications_df[
            "medication_name"
        ].value_counts()
    )

    print()

    print("Ongoing medication distribution:")
    print(
        concomitant_medications_df[
            "medication_ongoing"
        ].value_counts()
    )

print("=" * 50)



# ============================================================
# RAW DATA VERIFICATION
# ============================================================

import os

raw_folder = "../03_Raw data"

files_to_check = [
    "subjects_raw.csv",
    "medical_history_raw.csv",
    "visits_raw.csv",
    "vital_signs_raw.csv",
    "laboratory_raw.csv",
    "adverse_events_raw.csv",
    "concomitant_medications_raw.csv"
]

print("\n" + "=" * 60)
print("RAW DATA VERIFICATION")
print("=" * 60)

for file_name in files_to_check:

    file_path = os.path.join(raw_folder, file_name)

    if os.path.exists(file_path):

        df = pd.read_csv(file_path)

        print(f"\nFILE: {file_name}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print("Column names:")
        print(list(df.columns))

    else:
        print(f"\nMISSING FILE: {file_name}")

# ------------------------------------------------------------
# SUBJECT ID CHECK
# ------------------------------------------------------------

subjects_file = os.path.join(raw_folder, "subjects_raw.csv")
subjects_df = pd.read_csv(subjects_file)

print("\n" + "-" * 60)
print("SUBJECT ID CHECK")
print("-" * 60)

print(f"Total subject records: {len(subjects_df)}")
print(f"Unique subject IDs: {subjects_df['subject_id'].nunique()}")

duplicate_subjects = subjects_df[
    subjects_df["subject_id"].duplicated(keep=False)
]

if len(duplicate_subjects) == 0:
    print("Duplicate subject IDs: NONE")
else:
    print("Duplicate subject IDs FOUND:")
    print(duplicate_subjects["subject_id"].unique())

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)


# ============================================================
# CONTROLLED DATA QUALITY ISSUES
# ============================================================

import os

quality_folder = "../03_Raw data/quality_issues"

os.makedirs(quality_folder, exist_ok=True)

# ------------------------------------------------------------
# 1. Missing required value - Subjects
# ------------------------------------------------------------

subjects_dirty = subjects_df.copy()

subjects_dirty.loc[5, "site_id"] = pd.NA

subjects_dirty.to_csv(
    os.path.join(quality_folder, "subjects_dirty.csv"),
    index=False
)

# ------------------------------------------------------------
# 2. Impossible blood pressure - Vital Signs
# ------------------------------------------------------------

vitals_file = "../03_Raw data/vital_signs_raw.csv"
vitals_dirty = pd.read_csv(vitals_file)

vitals_dirty.loc[10, "systolic_bp"] = 300

vitals_dirty.to_csv(
    os.path.join(quality_folder, "vital_signs_dirty.csv"),
    index=False
)

# ------------------------------------------------------------
# 3. Duplicate subject record
# ------------------------------------------------------------

duplicate_subject = subjects_df.iloc[[20]].copy()

subjects_duplicate = pd.concat(
    [subjects_df, duplicate_subject],
    ignore_index=True
)

subjects_duplicate.to_csv(
    os.path.join(quality_folder, "subjects_duplicate.csv"),
    index=False
)

# ------------------------------------------------------------
# 4. AE starts before informed consent
# ------------------------------------------------------------

ae_file = "../03_Raw data/adverse_events_raw.csv"
ae_dirty = pd.read_csv(ae_file)

ae_dirty.loc[0, "ae_start_date"] = "2025-12-01"

ae_dirty.to_csv(
    os.path.join(quality_folder, "adverse_events_dirty.csv"),
    index=False
)

# ------------------------------------------------------------
# 5. AE missing end date while not ongoing
# ------------------------------------------------------------

ae_missing_end = pd.read_csv(ae_file)

ae_missing_end.loc[1, "ae_ongoing"] = "No"
ae_missing_end.loc[1, "ae_end_date"] = ""

ae_missing_end.to_csv(
    os.path.join(quality_folder, "adverse_events_missing_end_date.csv"),
    index=False
)

# ------------------------------------------------------------
# 6. Laboratory result outside reference range
# ------------------------------------------------------------

lab_file = "../03_Raw data/laboratory_raw.csv"
lab_dirty = pd.read_csv(lab_file)

lab_dirty.loc[0, "lab_result"] = 250
lab_dirty.loc[0, "abnormal_flag"] = "Normal"

lab_dirty.to_csv(
    os.path.join(quality_folder, "laboratory_dirty.csv"),
    index=False
)

# ------------------------------------------------------------
# 7. Medication end date before start date
# ------------------------------------------------------------

cm_file = "../03_Raw data/concomitant_medications_raw.csv"
cm_dirty = pd.read_csv(cm_file)

cm_dirty.loc[0, "medication_end_date"] = "2020-01-01"

cm_dirty.to_csv(
    os.path.join(quality_folder, "concomitant_medications_dirty.csv"),
    index=False
)

# ------------------------------------------------------------
# 8. Visit missing completion reason
# ------------------------------------------------------------

visit_file = "../03_Raw data/visits_raw.csv"
visits_dirty = pd.read_csv(visit_file)

# Find a missed visit
missed_rows = visits_dirty[
    visits_dirty["visit_status"] == "Missed"
]

if len(missed_rows) > 0:
    missed_index = missed_rows.index[0]
    visits_dirty.loc[
        missed_index,
        "visit_not_completed_reason"
    ] = ""

visits_dirty.to_csv(
    os.path.join(quality_folder, "visits_dirty.csv"),
    index=False
)

print("\n" + "=" * 60)
print("CONTROLLED DATA QUALITY ISSUES CREATED")
print("=" * 60)

print(f"Output folder: {quality_folder}")
print("\nFiles created:")

for file_name in os.listdir(quality_folder):
    print(f"- {file_name}")

print("\nIntentional issues include:")
print("- Missing required site")
print("- Impossible systolic blood pressure")
print("- Duplicate subject")
print("- AE before informed consent")
print("- AE missing end date")
print("- Laboratory result/reference inconsistency")
print("- Medication end date before start date")
print("- Missing reason for missed visit")

print("\nOriginal raw datasets were NOT modified.")
print("=" * 60)



# ============================================================
# VERIFY DQ-003 AND DQ-005
# ============================================================

print("\n" + "=" * 60)
print("VERIFYING DQ-003: DUPLICATE SUBJECT")
print("=" * 60)

duplicate_check = pd.read_csv("../03_Raw data/quality_issues/subjects_duplicate.csv")

duplicate_counts = duplicate_check["subject_id"].value_counts()
duplicates = duplicate_counts[duplicate_counts > 1]

print("Duplicate Subject IDs:")
print(duplicates)

print("\n" + "=" * 60)
print("VERIFYING DQ-005: AE MISSING END DATE")
print("=" * 60)

ae_check = pd.read_csv(
    "../03_Raw data/quality_issues/adverse_events_missing_end_date.csv"
)

print("\nRows where AE is Not Ongoing:")
print(ae_check[ae_check["ae_ongoing"].astype(str).str.strip().str.lower() == "no"][
    ["subject_id", "ae_term", "ae_ongoing", "ae_end_date"]
].to_string(index=False))

print("\nRows with blank AE End Date:")
print(
    ae_check[
        ae_check["ae_end_date"].isna()
        | (ae_check["ae_end_date"].astype(str).str.strip() == "")
    ][
        ["subject_id", "ae_term", "ae_ongoing", "ae_end_date"]
    ].to_string(index=False)
)

print("=" * 60)


import pandas as pd

ae = pd.read_csv("../03_Raw data/quality_issues/adverse_events_dirty.csv")
subjects = pd.read_csv("../03_Raw data/subjects_raw.csv")

ae["ae_start_date"] = pd.to_datetime(ae["ae_start_date"])
subjects["consent_date"] = pd.to_datetime(subjects["consent_date"])

check = ae.merge(
    subjects[["subject_id", "consent_date"]],
    on="subject_id",
    how="left"
)

issues = check[check["ae_start_date"] < check["consent_date"]]

print("\nDQ-004 — AE START DATE BEFORE CONSENT")
print("=" * 60)
print(
    issues[
        ["subject_id", "ae_term", "ae_start_date", "consent_date"]
    ].to_string(index=False)
)
print("=" * 60)