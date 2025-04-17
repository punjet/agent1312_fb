from prometheus_client import Counter, Gauge, start_http_server
from modules.config_loader import settings

# метрики
ACCOUNTS_CREATED = Counter('fb_accounts_created', 'Количество созданных акаунтов')
KYC_FAIL = Counter('fb_kyc_fail', 'Количество не прошедших KYC')
FIRSTBILL_SUCCESS = Counter('fb_firstbill_success', 'Количество успешных первобилов')
ACTIVE_ACCOUNTS = Gauge('fb_active_accounts', 'Текущее число активных акаунтов')

# старт Prometheus
start_http_server(8000)