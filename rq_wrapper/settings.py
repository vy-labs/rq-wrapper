import os

app_name = os.getenv('APPLICATION') or 'Unknown'
app_type = os.getenv('APPLICATION_TYPE') or 'RqWorker'
log_level = os.getenv('LOG_LEVEL') or 'INFO'
environment = os.getenv('ENVIRONMENT') or 'DEVELOPMENT'
namespace = os.getenv('RQ_NAMESPACE') or os.getenv('JOB_ID') or 'default'
