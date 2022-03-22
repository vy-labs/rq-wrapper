import os

app_name = os.getenv('APP_NAME') or 'Unknown'
app_type = os.getenv('APP_TYPE') or 'RqWorker'
log_level = os.getenv('LOG_LEVEL') or 'INFO'
environment = os.getenv('ENVIRONMENT') or 'DEVELOPMENT'
namespace = os.getenv('RQ_NAMESPACE') or os.getenv('JOB_ID') or 'default'
