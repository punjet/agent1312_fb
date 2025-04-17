import requests, time

class SMSActivator:
    def __init__(self, api_key):
        self.key = api_key
        self.base='https://api.helper20sms.ru'

    def get_number(self):
        r = requests.post(f"{self.base}/getNumber", data={'api_key':self.key,'service':'fb'})
        return r.json()['number']

    def wait_code(self, number, timeout=120):
        start=time.time()
        while time.time()-start<timeout:
            r = requests.get(f"{self.base}/getMessages", params={'api_key':self.key,'number':number})
            msgs=r.json()
            if msgs:
                return msgs[0]['code']
            time.sleep(5)
        raise TimeoutError('No SMS code')