from modules.playwright_worker import run_action

async def check_identity(acc: dict) -> dict:
    res = await run_action(acc, action='check_identity')
    acc['kyc_status'] = res.get('kyc_status')
    return acc

async def check_business(acc: dict) -> dict:
    res = await run_action(acc, action='check_business')
    acc['kyc_status'] = res.get('kyc_status')
    return acc

async def check_payment(acc: dict) -> dict:
    res = await run_action(acc, action='check_payment')
    acc['kyc_status'] = res.get('kyc_status')
    return acc

async def check_policies(acc: dict) -> dict:
    res = await run_action(acc, action='check_policies')
    acc['kyc_status'] = res.get('kyc_status')
    return acc