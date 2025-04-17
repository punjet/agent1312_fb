import asyncio
from modules.tempmail_async import create_email, wait_for_code
from modules.sms_activator_async import SMSAsync
from modules.tor_manager import TorManager
from modules.password_manager import encrypt_password
from modules.logger import logger

async def create_account_batch(n: int):
    sms = SMSAsync()
    tor = TorManager()
    created = []
    for i in range(n):
        if settings.use_tor:
            tor.new_identity()
        email = await create_email()
        password = uuid.uuid4().hex[:12]
        # тут Playwright можно использовать, но для простоты — сохраняем
        code_email = await wait_for_code(email)
        number = await sms.get_number()
        code_sms = await sms.wait_code(number)
        acc = {
            'login': email,
            'password': encrypt_password(password),
            'phone': number,
            'session': None,
            'kyc_status': None,
        }
        logger.info("Account created", email=email)
        created.append(acc)
    return created