# FILE-INTEGRITY-CHECKER

*COMPANY*: CODTECH IT SOLUTIONS

*NAME*: GYANCHAND YADAV

*INTERN ID*: CT12DA331

*DOMAIN*:  CYBER SECURITY & ETHICAL HACKING

*DURATION*: 12 WEEKS

*MENTOR*: NEELA SANTOSH

## Develop a Python-based tool to monitor the integrity of files within a specified directory. The tool should be capable of generating a secure baseline of file hashes and later verifying the current state of the directory against that baseline to detect unauthorized or accidental changes.

Key Features:

Baseline Initialization (init)

Recursively scan all files in the target directory.

Generate SHA-256 hashes for each file.

Save the hash data in a JSON file (file_integrity_baseline.json) as a trusted reference snapshot.

Integrity Check (check)

Re-scan the current state of the directory.

Compare with the previously saved baseline.

Identify and report:

New files (present now but not in the baseline)

Deleted files (missing now but present in the baseline)

Modified files (present in both but with different hashes)

Log all changes with timestamps to file_integrity_log.txt.
