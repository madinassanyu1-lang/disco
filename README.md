# disco

⚠️ **Safety notice**: This automation framework is for authorized test environments only. Set environment variable `TEST_ENVIRONMENT=true` before running.

## Quickstart

- Install dependencies: `pip install -r requirements.txt`
- Provide a sample input: `sample_inputs/sample.csv`
- Run: `python run.py sample_inputs/sample.csv`

The repository includes scaffolding for:
- Session management (fresh per-run contexts, UA rotation, proxy validation)
- Human-like interactions (typing, micro-pauses, safe clicks)
- Page-state detection and dynamic waits
- Error auditing and self-healing suggestions
- Structured outputs: `outputs/` and logs

Refer to `automation/` for module details.

---

## Security & safety checklist ⚠️
- Confirm runs are in authorized test environments only (set `TEST_ENVIRONMENT=true`).
- Do not run against production accounts or real user data.
- Abort on CAPTCHA or bot detection—do not attempt bypass.
- Rotate proxies and validate health before use.

## Alerts & notifications 🔔
- Alerts are disabled by default. Enable with `ENABLE_ALERTS=true`.
- Slack webhook: set `SLACK_WEBHOOK_URL` (recommended to store in secrets).
- PagerDuty: set `PAGERDUTY_ROUTING_KEY` for Events API v2 if you want urgent incidents.
- Alerts are non-blocking and best-effort; retries have a small cap and backoff.

## CLI options
- `python run.py <input_path>` — default behavior: one session per record (configurable via `SESSION_PER_RECORD` in environment).

## Files created during runs
- `outputs/` — success/failed exports
- `error_audit.log` — structured error lines
- `upgrade_suggestions.txt` — suggested mitigations for recurring issues
- `execution_summary.json` — audit-ready run summary
