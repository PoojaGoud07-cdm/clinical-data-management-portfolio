\# End-to-End Clinical Data Management Portfolio Project



\## Project Overview



This project demonstrates an end-to-end Clinical Data Management (CDM) workflow for a synthetic Phase II clinical trial. The project covers clinical data collection, CRF design, data quality review, SQL validation, query management, reconciliation, documentation, and safety analytics.



\## Study Overview



\- Study ID: ONC-2026-001

\- Study Phase: Phase II

\- Therapeutic Area: Type 2 Diabetes

\- Study Type: Randomized, double-blind, placebo-controlled

\- Investigational Product: ABC-101

\- Synthetic Subjects: 500

\- Study Sites: 10

\- Treatment Arms:

&#x20; - ABC-101 50 mg

&#x20; - ABC-101 100 mg

&#x20; - Placebo



\## Objectives



\- Design clinical data collection instruments

\- Build and validate CRFs

\- Generate and review synthetic clinical trial data

\- Perform data quality checks

\- Validate data using SQL

\- Document and manage data queries

\- Perform cross-domain data reconciliation

\- Create clinical data management documentation

\- Develop a Power BI safety analytics dashboard



\## Tools \& Technologies



\- REDCap

\- Microsoft Excel

\- Python

\- PostgreSQL

\- SQL

\- Power BI

\- Git

\- GitHub



\## Clinical Data Domains



\- Demographics

\- Medical History

\- Study Visits

\- Vital Signs

\- Laboratory

\- Adverse Events

\- Concomitant Medications



\## Project Workflow



1\. Study protocol and synopsis development

2\. Data Management Plan development

3\. CRF specification and edit-check design

4\. REDCap CRF implementation

5\. Synthetic clinical data generation

6\. Data quality issue creation and review

7\. PostgreSQL data loading and validation

8\. Query management

9\. Cross-domain data reconciliation

10\. Data review and closeout documentation

11\. Power BI safety and data quality analytics

12\. Git/GitHub portfolio development



\## Data Quality Management



Controlled data quality issues were created to demonstrate common clinical data review scenarios, including:



\- Missing required data

\- Duplicate records

\- Out-of-range values

\- Date inconsistencies

\- Cross-field inconsistencies

\- Missing visit information



The issues were documented, queried, reviewed, and tracked through resolution or review.



\## SQL Validation



PostgreSQL was used to perform validation checks including:



\- Duplicate record checks

\- Required field checks

\- Range validation

\- Orphan record checks

\- Date consistency checks

\- Cross-field consistency checks

\- Subject and visit linkage checks



\## Query Management



Eight simulated clinical data queries were documented and tracked from issue identification through response and resolution.



\## Data Reconciliation



Sixteen reconciliation checks were performed across clinical data domains.



\- 15 checks passed

\- 1 check remains under review



The outstanding issue involves missing Visit Name values for 137 adverse event records. Subject-level linkage was confirmed, but visit-level linkage could not be established from the available data.



\## Power BI Dashboard



The Power BI dashboard provides clinical trial data management and safety analytics, including:



\- Total subjects

\- Total study visits

\- Total adverse events

\- Serious adverse events

\- Abnormal laboratory percentage

\- Subjects with adverse events

\- Laboratory result distribution

\- Study visit status

\- Treatment distribution

\- Adverse event severity

\- Adverse event seriousness

\- Adverse event relationship

\- Study site distribution

\- Subject demographics



\## Key Results



\- 500 synthetic subjects

\- 3,230 study visit records

\- 137 adverse event records

\- 120 subjects with adverse events

\- 4 serious adverse events

\- 18,852 laboratory records

\- 46.9% abnormal laboratory results

\- 702 concomitant medication records

\- 1,012 medical history records



\## Outstanding Data Issue



The final reconciliation identified 137 adverse event records with missing Visit Name values.



Subject-level linkage was confirmed, but visit-level linkage was not established. This issue remains documented for further review and is not classified as resolved.



\## Skills Demonstrated



\- Clinical Data Management

\- CRF Development

\- Data Validation

\- Data Quality Management

\- Query Management

\- Data Reconciliation

\- SQL/PostgreSQL

\- Excel

\- Python

\- Power BI

\- Clinical Trial Documentation

\- Safety Data Review

\- Git/GitHub



\## Project Structure



```text

01\_Protocol

02\_CRF's

03\_Raw data

04\_Sql

05\_Data quality

06\_Query management

07\_Reconciliation

08\_Documentation

09\_PowerBI

10\_Final dataset



