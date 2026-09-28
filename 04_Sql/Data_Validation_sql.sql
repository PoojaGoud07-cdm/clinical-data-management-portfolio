CREATE TABLE raw.subjects (
    study_id VARCHAR(50),
    subject_id VARCHAR(20),
    site_id VARCHAR(10),
    consent_date DATE,
    date_of_birth DATE,
    age INTEGER,
    sex VARCHAR(30),
    race VARCHAR(100),
    ethnicity VARCHAR(50),
    height_cm NUMERIC(5,1),
    weight_kg NUMERIC(5,1),
    treatment VARCHAR(50),
    screening_status VARCHAR(30),
    screen_fail_reason TEXT
);



select count(*) as subject_count
from raw.subjects;

select * from raw.subjects
limit 10 ;

CREATE TABLE raw.medical_history (
    subject_id VARCHAR(20),
    medical_condition VARCHAR(150),
    condition_category VARCHAR(50),
    condition_start_date DATE,
    condition_end_date DATE,
    condition_ongoing VARCHAR(10),
    comments TEXT
);

select  count (*) as medical_history_count
from raw.medical_history;

select * from raw.medical_history
limit 10;

CREATE TABLE raw.visits (
    subject_id VARCHAR(20),
    visit_name VARCHAR(30),
    visit_date DATE,
    visit_status VARCHAR(20),
    treatment_assignment VARCHAR(50),
    visit_completed VARCHAR(10),
    visit_not_completed_reason TEXT,
    visit_comments TEXT
);

select count (*) as visits_count
from raw.visits;

select * from raw.visits
limit 10;

CREATE TABLE raw.vital_signs (
    subject_id VARCHAR(20),
    visit_name VARCHAR(30),
    visit_date DATE,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    heart_rate INTEGER,
    respiratory_rate INTEGER,
    temperature_c NUMERIC(4,1),
    weight_kg NUMERIC(5,1),
    comments TEXT
);

select count(*) as vital_signs_count
from raw.vital_signs;

select * from raw.vital_signs
limit 10;

CREATE TABLE raw.laboratory (
    subject_id VARCHAR(20),
    visit_name VARCHAR(30),
    lab_collection_date DATE,
    lab_test VARCHAR(50),
    lab_result NUMERIC(10,2),
    lab_unit VARCHAR(20),
    reference_low NUMERIC(10,2),
    reference_high NUMERIC(10,2),
    abnormal_flag VARCHAR(10),
    lab_comments TEXT
);

select count (*) as laboratory_count
from raw.laboratory;

select * from raw.laboratory
limit 10;

CREATE TABLE raw.adverse_events (
    subject_id VARCHAR(20),
    visit_name VARCHAR(30),
    ae_term VARCHAR(150),
    ae_start_date DATE,
    ae_end_date DATE,
    ae_ongoing VARCHAR(10),
    ae_seriousness VARCHAR(20),
    ae_severity VARCHAR(20),
    ae_relationship VARCHAR(50),
    ae_action VARCHAR(50),
    ae_outcome VARCHAR(50),
    ae_comments TEXT
);

select count(*) as adverse_events_count
from raw.adverse_events;

select * from raw.adverse_events
limit 10;

CREATE TABLE raw.concomitant_medications (
    subject_id VARCHAR(20),
    medication_name VARCHAR(150),
    medication_indication VARCHAR(150),
    medication_start_date DATE,
    medication_end_date DATE,
    medication_ongoing VARCHAR(10),
    medication_dose_frequency VARCHAR(100),
    comments TEXT
);

select count(*) as concomitant_medications_count
from raw.concomitant_medications;

select * from raw.concomitant_medications
limit 10;

SELECT 'subjects' AS table_name, COUNT(*) AS record_count
FROM raw.subjects

UNION ALL

SELECT 'medical_history', COUNT(*)
FROM raw.medical_history

UNION ALL

SELECT 'visits', COUNT(*)
FROM raw.visits

UNION ALL

SELECT 'vital_signs', COUNT(*)
FROM raw.vital_signs

UNION ALL

SELECT 'laboratory', COUNT(*)
FROM raw.laboratory

UNION ALL

SELECT 'adverse_events', COUNT(*)
FROM raw.adverse_events

UNION ALL

SELECT 'concomitant_medications', COUNT(*)
FROM raw.concomitant_medications

ORDER BY table_name;


SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'raw'
ORDER BY table_name;

-- clean schemas
-- clean.subjects

CREATE TABLE clean.subjects AS
SELECT
    study_id,
    subject_id,
    site_id,
    consent_date,
    date_of_birth,
    age,
    sex,
    race,
    ethnicity,
    height_cm,
    weight_kg,
    treatment,
    screening_status,
    screen_fail_reason
FROM raw.subjects
WHERE subject_id IS NOT NULL
  AND TRIM(subject_id) <> '';

select count(*) as clean_subjects_count
from clean.subjects;

--duplicate records = 0
select subject_id , count (*) as record_count
from clean.subjects
group by subject_id
having count(*) > 1;

-- missing required values = none
SELECT
    COUNT(*) FILTER (WHERE subject_id IS NULL OR TRIM(subject_id) = '') AS missing_subject_id,
    COUNT(*) FILTER (WHERE site_id IS NULL OR TRIM(site_id) = '') AS missing_site_id,
    COUNT(*) FILTER (WHERE consent_date IS NULL) AS missing_consent_date,
    COUNT(*) FILTER (WHERE date_of_birth IS NULL) AS missing_date_of_birth,
    COUNT(*) FILTER (WHERE age IS NULL) AS missing_age,
    COUNT(*) FILTER (WHERE sex IS NULL OR TRIM(sex) = '') AS missing_sex,
    COUNT(*) FILTER (WHERE treatment IS NULL OR TRIM(treatment) = '') AS missing_treatment,
    COUNT(*) FILTER (WHERE screening_status IS NULL OR TRIM(screening_status) = '') AS missing_screening_status
FROM clean.subjects;

-- validate subject age = none
select
 min(age) as minimum_age,
 max(age) as maximum_age,
 count(*) filter (where age < 18 or age > 100) as invalid_age_count
from clean.subjects; 

-- validate height and weight = none
select
  min(height_cm) as minimum_height_cm,
  max(height_cm) as maximum_height_cm,
  count(*) filter(where height_cm < 100 or height_cm > 250) as invalid_height_count,
  min(weight_kg) as minimum_weight_kg,
  max(weight_kg) as maximum_weight_kg,
  count(*) filter (where weight_kg < 30 or weight_kg > 250) as invalid_weight_count
from clean.subjects;  

-- validate treatment assignments = 0
select treatment, 
  count(*) as subject_count
from clean.subjects
group by treatment
order by treatment;

select distinct treatment
from clean.subjects
where treatment not in ('ABC-101 100 mg' , 'ABC-101 50 mg' , 'Placebo');

-- treatment-arm counts - 500
select treatment, 
  count(*) as subject_count
from clean.subjects
group by treatment
order by treatment;

-- final clean subjects integrety tests
select
   count(*) as total_records,
   count(distinct subject_id) as unique_records
from clean.subjects;

-- cleans.medical_history

CREATE TABLE clean.medical_history AS
SELECT
    subject_id,
    medical_condition,
    condition_category,
    condition_start_date,
    condition_end_date,
    condition_ongoing,
    comments
FROM raw.medical_history
WHERE subject_id IS NOT NULL
  AND TRIM(subject_id) <> '';


select count(*) as clean_medical_history_count
from clean.medical_history;

-- validate medical_history dates

SELECT
    COUNT(*) FILTER (
        WHERE condition_start_date > CURRENT_DATE
    ) AS future_start_dates, --Condition doesn't start in the future.
    COUNT(*) FILTER (
        WHERE condition_end_date IS NOT NULL
          AND condition_end_date < condition_start_date 
    ) AS end_before_start, --End date isn't before start date.
    COUNT(*) FILTER (
        WHERE condition_ongoing = 'No'
          AND condition_end_date IS NULL
    ) AS missing_end_date_when_not_ongoing,--Non-ongoing conditions have an end date.
    COUNT(*) FILTER (
        WHERE condition_ongoing = 'Yes'
          AND condition_end_date IS NOT NULL
    ) AS end_date_present_when_ongoing --Ongoing conditions don't have an end date.
FROM clean.medical_history;


--Final Medical history record check

select count (*) as total_records,
       count(distinct subject_id) as unique_records
from clean.medical_history;

-- clean.study_visits
CREATE TABLE clean.visits AS
SELECT
    subject_id,
    visit_name,
    visit_date,
    visit_status,
    treatment_assignment,
    visit_completed,
    visit_not_completed_reason,
    visit_comments
FROM raw.visits
WHERE subject_id IS NOT NULL
  AND TRIM(subject_id) <> '';

select count(*) as clean_visit_count
from clean.visits;

select * from clean.visits
limit 10;
-- duplicate visit records

select subject_id,
       visit_name,
	   visit_date,
	   count(*) as duplicate_records
from clean.visits
group by subject_id , visit_name, visit_date
having count(*) > 1;

-- finding orphan_visit_counts
select count(*) as orphan_visit_count
from clean.visits v
    left join clean.subjects s
	   on v.subject_id = s.subject_id
	where s.subject_id is null;

-- visit status consistency
select count(*) as inconsistent_status_count
from clean.visits
where (visit_status = 'Complete' and visit_completed <> 'Yes') or
      (visit_status = 'Missed' and visit_completed <> 'No');

-- missing visits
select count(*) as missing_missed_visit_reason
from clean.visits
where visit_status = 'Missed' and
      (visit_completed is null or trim(visit_not_completed_reason) = '');

-- visit dates
select count(*) as visit_before_consent
from clean.visits v
join clean.subjects s
  on v.subject_id = s.subject_id
where v.visit_date < s. consent_date;

--final visits check
select 
      count (*) filter(where subject_id is null or trim(subject_id) = '' ) as missing_subject_id,
	  count (*) filter(where visit_name is null or trim(visit_name) = '') as missing_visit_name,
	  count(*) filter(where visit_date is null) as missing_visit_date
from clean.visits;

-- clean.vital_signs
CREATE TABLE clean.vital_signs AS
SELECT
    subject_id,
    visit_name,
    visit_date,
    systolic_bp,
    diastolic_bp,
    heart_rate,
    respiratory_rate,
    temperature_c,
    weight_kg,
    comments
FROM raw.vital_signs
WHERE subject_id IS NOT NULL
  AND TRIM(subject_id) <> '';

select count(*) as vital_signs_count
from clean.vital_signs;

-- duplicate records
select subject_id , visit_name , visit_date,
       count(*) as duplicate_records
from clean.vital_signs
group by subject_id, visit_name, visit_date
having count(*) > 1;

-- orphan vital signs count
select count(*) as orphan_vital_signs_count
from clean.vital_signs v
 left join clean.subjects s
       on v.subject_id = s.subject_id
where s.subject_id is null;

-- blood pressure check
select
     count(*) filter(
                   where systolic_bp < 70 or systolic_bp > 250) as invalid_systolic_bp,
	 count(*) filter(
                   where diastolic_bp < 40 or diastolic_bp > 150) as invalid_diastolic_bp
from clean.vital_signs;

--heart rate(30-200bpm) and respiratory rate(8-40 breaths/min)
select
      count(*) filter(
                   where heart_rate < 30 or heart_rate > 200) as invalid_heart_rate,
	  count(*) filter(
                   where respiratory_rate < 8 or respiratory_rate > 40) as invalid_respiratory_rate
from clean.vital_signs;

--weight(30-250kg) temperature(30-45°C)
select 
     count(*) filter( 
                  where temperature_c < 30 or temperature_c > 45) as invalid_temperature,
	 count(*) filter(
	              where weight_kg < 30 or weight_kg > 250) as invalid_weight
from clean.vital_signs;

-- required field check
select
     count(*) filter(where subject_id is null or trim(subject_id) = '') as missing_subject_id,
	 count(*) filter(where visit_name is null or trim(visit_name) = '') as missing_visit_name,
	 count(*) filter(where visit_date is null)
from clean.vital_signs;

--unmatched vital signs for visits
select count(*) as unmatched_vital_signs_visit
from clean.vital_signs vs
  left join clean.visits v
         on vs.subject_id = v.subject_id and
		    vs.visit_name = v.visit_name
where v.subject_id is null;

--clean.laboratory
CREATE TABLE clean.laboratory AS
SELECT
    subject_id,
    visit_name,
    lab_collection_date,
    lab_test,
    lab_result,
    lab_unit,
    reference_low,
    reference_high,
    abnormal_flag,
    lab_comments
FROM raw.laboratory
WHERE subject_id IS NOT NULL
  AND TRIM(subject_id) <> '';

select count(*) as clean_laboratory_count
from clean.laboratory;

-- duplicate records
select subject_id , visit_name, lab_collection_date , lab_test,
       count(*) as duplicate_records
from clean.laboratory
group by subject_id , visit_name, lab_collection_date , lab_test
having count(*) > 1;

-- orphan laboratory records
select count(*) as orphan_laboratory_count
from clean.laboratory l
   left join clean.subjects s
         on l.subject_id = s.subject_id
where s.subject_id is null;

-- inconsistent laboratory results
select count(*) as inconsistent_lab_results
from clean.laboratory
   where (lab_result > reference_high and abnormal_flag <> 'High') or
         (lab_result < reference_low and abnormal_flag <> 'Low') or
		 (lab_result between reference_low and reference_high and abnormal_flag <> 'Normal');

-- missing required fields
select
     count(*) filter(where subject_id is null or trim(subject_id) = '') as missed_subject_id,
	 count(*) filter(where visit_name is null or trim(visit_name) = '') as missed_visit_name,
	 count(*) filter(where lab_collection_date is null) as missed_lab_collection_date,
	 count(*) filter(where lab_test is null or trim(lab_test) = '') as missed_lab_test,
	 count(*) filter(where lab_result is null) as missed_lab_results
from clean.laboratory;

-- unmatched lab visits
select count(*) as unmatched_lab_visits
from clean.laboratory l
   left join clean.visits v
         on l.subject_id = v.subject_id and
		    l.visit_name = v.visit_name
where v.subject_id is null;

-- invalid reference ranges
select count(*) as invalid_reference_range
from clean.laboratory
where reference_low > reference_high;

-- clean.adverse_events
CREATE TABLE clean.adverse_events AS
SELECT
    subject_id,
    visit_name,
    ae_term,
    ae_start_date,
    ae_end_date,
    ae_ongoing,
    ae_seriousness,
    ae_severity,
    ae_relationship,
    ae_action,
    ae_outcome,
    ae_comments
FROM raw.adverse_events
WHERE subject_id IS NOT NULL
  AND TRIM(subject_id) <> '';


select count(*) as adverse_events_count
from clean.adverse_events;

-- duplicate records
select 
    subject_id,
    visit_name,
    ae_term,
    ae_start_date,
	count(*) as duplicate_records
from clean.adverse_events
group by subject_id,
    visit_name,
    ae_term,
    ae_start_date
having count(*) > 1;

-- orphan records
select count(*) as orphan_ae_records
from clean.adverse_events ae
   left join clean.subjects s
          on ae.subject_id = s.subject_id
where s.subject_id is null;

-- ongoing vs end dates
select count(*) as ongoing_date_errors
from clean.adverse_events
where (ae_ongoing = 'No' and ae_end_date is null) or
      (ae_ongoing = 'Yes' and ae_end_date is not null);

-- date sequence
select count(*) as invalid_ae_dates
from clean.adverse_events
where ae_end_date is not null
     and ae_end_date < ae_start_date;

--ae start date vs consent date
select count(*) as ae_before_consent
from clean.adverse_events ae
  join clean.subjects s
    on ae.subject_id = s.subject_id
where ae.ae_start_date < s.consent_date;

--missing field check
select
    count (*) filter(where subject_id is null or trim (subject_id) = '') as missed_subject_id,
	count (*) filter(where ae_term is null or trim (ae_term) = '') as missed_ae_term,
	count (*) filter(where ae_start_date is null) as missed_ae_start_date,
	count (*) filter(where ae_ongoing is null or trim(ae_ongoing) = '') as missed_ae_ongoing,
	count (*) filter(where ae_severity is null or trim(ae_severity) = '') as missed_ae_severity
from clean.adverse_events;

-- unmatched visits
select count(*) as unmatched_visits
from clean.adverse_events ae
  left join clean.visits v
       on ae.subject_id = v.subject_id and
	      ae.visit_name = v.visit_name
where v.subject_id is null;

SELECT
    ae.subject_id,
    ae.visit_name,
    v.visit_name AS matching_visit
FROM clean.adverse_events ae
LEFT JOIN clean.visits v
    ON ae.subject_id = v.subject_id
    AND ae.visit_name = v.visit_name
LIMIT 20;

select count(*) as missing_ae_visit_names
from clean.adverse_events
where visit_name is null or trim (visit_name) = '';

-- ae subject_id not in visits
select count(*) as ae_subject_id_not_in_visits
from clean.adverse_events ae
   left join clean.visits v
         on ae.subject_id = v.subject_id
where v.subject_id is null;

--severity count
select ae_severity ,
      count (*) as record_count
from clean.adverse_events
group by ae_severity
order by ae_severity;

--seriousness records
select ae_seriousness,
       count (*) as record_count
from clean.adverse_events
group by ae_seriousness
order by ae_seriousness;

-- relationship values
select ae_relationship,
      count(*) as record_count
from clean.adverse_events
group by ae_relationship
order by ae_relationship;

--action values
select ae_action,
      count(*) as record_count
from clean.adverse_events
group by ae_action
order by ae_action;

--outcome values
select ae_outcome,
       count(*) as record_count
from clean.adverse_events
group by ae_outcome
order by ae_outcome;

-- record count integrity
select count(*) as ae_total_records,
       count(distinct subject_id) as unique_subject_id
from clean.adverse_events;

--clean.concomitant medications
CREATE TABLE clean.concomitant_medications AS
SELECT
    subject_id,
    medication_name,
    medication_indication,
    medication_start_date,
    medication_end_date,
    medication_ongoing,
    medication_dose_frequency,
    comments
FROM raw.concomitant_medications
WHERE subject_id IS NOT NULL
  AND TRIM(subject_id) <> '';

select count(*) as total_cm_records
from clean.concomitant_medications;

--duplicate records
select subject_id, medication_name, medication_start_date,
       count(*) as duplicate_records
from clean.concomitant_medications
group by subject_id, medication_name, medication_start_date
having count(*) > 1;

-- orphan subjects
select count(*) as orphan_cm_records
from clean.concomitant_medications cm
   left join clean.subjects s
          on cm.subject_id = s.subject_id
where s.subject_id is null;

--ongoing vs end date
select count(*) as ongoing_date_errors
from clean.concomitant_medications
where (medication_ongoing = 'No' and medication_end_date is null) or
      (medication_ongoing = 'Yes' and medication_end_date is not null);


--invalid dates
select count(*) as invalid_dates
from clean.concomitant_medications
where medication_end_date is null and 
      medication_end_date < medication_start_date;

-- missing fields check
select
     count(*) filter(where subject_id is null or trim(subject_id) = '') as missed_subject_id,
	 count(*) filter(where medication_name is null or trim(medication_name) = '') as missed_medication_name,
	 count(*) filter(where medication_start_date is null) as missed_medication_start_date,
	 count(*) filter(where medication_ongoing is null or trim(medication_ongoing) = '') as missed_medication_ongoing
from clean.concomitant_medications;

--subjects not in visits
select count(*) as cm_subjects_not_in_visits
from clean.concomitant_medications cm
   left join clean.visits v
         on cm.subject_id = v.subject_id
where v.subject_id is null;

-- record count integrity
select count(*) as total_cm_records,
       count(distinct subject_id) as unique_subjects
from clean.concomitant_medications;











	   