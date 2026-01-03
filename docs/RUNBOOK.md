# Runbook (authorized test environments only)

## Preflight checks
- Ensure `TEST_ENVIRONMENT=true` is set in environment or secrets before running.
- Confirm proxy list and health-check endpoints are reachable (if using proxies).
- Ensure `sample_inputs/` contains valid TSV/CSV/XLSX test files.

## Running a test batch (local)
1. Install deps: `pip install -r requirements.txt`
2. Run: `python run.py sample_inputs/sample.csv`

## Handling failures
- Check `error_audit.log` for structured entries with classification and session_id.
- If a recurring issue is detected, `upgrade_suggestions.txt` will contain an actionable recommendation.
- For CAPTCHA or bot detection, abort and escalate to security team; do not attempt bypass.

## Emergency stop
- If automation misbehaves, kill running processes and rotate the test environment token.

## CI considerations
- CI runs include unit tests only; any browser-based runs must be executed in authorized infra only and guarded by the `TEST_ENVIRONMENT` flag.
