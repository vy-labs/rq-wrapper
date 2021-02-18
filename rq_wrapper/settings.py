import os

namespace = os.getenv('RQ_NAMESPACE') or os.getenv('JOB_ID')
