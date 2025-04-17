import requests, time

class TempMailClient:
    def __init__(self):
        self.base = 'https://api.temp-mail.org/request'

    def create_email(self):
        # запрос нового почтового ящика
        resp = requests.get(f"{self.base}/domains/")
        domain = resp.json()[0]
        local = uuid.uuid4().hex[:8]
        return f"{local}@{domain}"

    def wait_for_code(self, email, timeout=120):
        # проверяем почту каждые 5 сек
        start=time.time()
        while time.time()-start<timeout:
            msgs = requests.get(f"{self.base}/mail/id/{email}/").json()
            for m in msgs:
                if 'код' in m['subject']:
                    return extract_code(m['body'])
            time.sleep(5)
        raise TimeoutError('No email code')