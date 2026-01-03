import os

CONFIG = {
    # Must be explicitly enabled in authorized test environments
    # e.g.: export TEST_ENVIRONMENT=true
    "TEST_ENVIRONMENT": os.environ.get("TEST_ENVIRONMENT", "false").lower() == "true",

    # Retry/backoff
    "MAX_RETRIES": int(os.environ.get("MAX_RETRIES", 3)),
    "BACKOFF_BASE_SECONDS": float(os.environ.get("BACKOFF_BASE_SECONDS", 0.5)),
    "BACKOFF_MAX_SECONDS": float(os.environ.get("BACKOFF_MAX_SECONDS", 30)),

    # Session/workflow
    "SESSION_PER_RECORD": os.environ.get("SESSION_PER_RECORD", "true").lower() == "true",

    # Logging
    "ERROR_AUDIT_LOG": os.environ.get("ERROR_AUDIT_LOG", "error_audit.log"),
    "UPGRADE_SUGGESTIONS": os.environ.get("UPGRADE_SUGGESTIONS", "upgrade_suggestions.txt"),
    "EXECUTION_SUMMARY": os.environ.get("EXECUTION_SUMMARY", "execution_summary.json"),

    # Proxy health endpoint (authorized infra only)
    "PROXY_HEALTH_TEST_URL": os.environ.get("PROXY_HEALTH_TEST_URL", "https://httpbin.org/ip"),

    # Alerts
    "ENABLE_ALERTS": os.environ.get("ENABLE_ALERTS", "false").lower() == "true",
    "SLACK_WEBHOOK_URL": os.environ.get("SLACK_WEBHOOK_URL"),
    "PAGERDUTY_ROUTING_KEY": os.environ.get("PAGERDUTY_ROUTING_KEY"),
    "NOTIFIER_MAX_RETRIES": int(os.environ.get("NOTIFIER_MAX_RETRIES", 3)),
}
