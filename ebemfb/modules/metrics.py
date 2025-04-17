# Пример экспорта дополнительных метрик
# Подключается в важных модулях при каждом успехе/ошибке
from prometheus_client import Summary
REQUEST_TIME = Summary('fb_request_latency_seconds', 'Latency of external requests')