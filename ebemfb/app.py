import asyncio
import sys
from typing import List, Optional

import typer
from modules.config_loader import settings
from modules.tor_manager import TorManager
from modules.proxy_api_client import fetch_proxy
from modules.proxy_manager_async import health_check
from modules.account_creator import create_account_batch
from modules.account_warmer import warm_batch
from modules.account_classifier import (
    check_identity, check_business, check_payment, check_policies
)
from modules.playwright_worker import run_action
from modules.ad_manager import TestAdVerifier, MainCampaignAgent
from modules.account_visualizer import visualize
from modules.logger import logger

typer_app = typer.Typer(help="CLI для управления Facebook Pervobil Ideal")


def _print_header():
    typer.secho("\nFacebook Pervobil Ideal - CLI Utility", fg=typer.colors.CYAN, bold=True)


@typer_app.command()
def init(
    mode: str = typer.Option("proxy", help="Режим соединения: 'tor' или 'proxy'"),
    count: int = typer.Option(10, help="Число тестовых попыток"),
):
    """
    Проверка соединения через Tor или сторонний прокси.
    """
    _print_header()
    loop = asyncio.get_event_loop()
    if mode == "tor":
        tm = TorManager()
        successes = 0
        for i in range(count):
            tm.new_identity()
            ok = loop.run_until_complete(health_check(None))
            if ok:
                successes += 1
        rate = successes / count * 100
        typer.secho(f"Tor connectivity success: {rate:.1f}% ({successes}/{count})\n", fg=typer.colors.GREEN)
    else:
        successes = 0
        for i in range(count):
            proxy = loop.run_until_complete(fetch_proxy())
            ok = loop.run_until_complete(health_check(proxy))
            if ok:
                successes += 1
        rate = successes / count * 100
        typer.secho(f"Proxy connectivity success: {rate:.1f}% ({successes}/{count})\n", fg=typer.colors.GREEN)


@typer_app.command()
def create(
    batch: int = typer.Option(None, help="Сколько аккаунтов создать (batch_size из конфига по умолчанию)")
):
    """
    Создание и регистрация Facebook-аккаунтов.
    """
    _print_header()
    n = batch or settings.batch_size
    accounts = asyncio.run(create_account_batch(n))
    typer.secho(f"Создано {len(accounts)} аккаунтов", fg=typer.colors.GREEN)
    for acc in accounts:
        typer.echo(f" - {acc['login']} | phone: {acc['phone']}")


@typer_app.command()
def warm(
    logins: List[str] = typer.Argument(..., help="Список логинов для прогрева")
):
    """
    Прогрев ранее созданных аккаунтов по логинам.
    """
    _print_header()
    # Предполагаем загрузку аккаунтов из БД или файла
    # Здесь просто эмуляция: передаем list of dicts
    accounts = [{ 'login': l } for l in logins]
    warmed = asyncio.run(warm_batch(accounts))
    typer.secho(f"Прогрето {len(warmed)} аккаунтов", fg=typer.colors.GREEN)


@typer_app.command()
def kyc(
    logins: List[str] = typer.Argument(..., help="Список логинов для проверки KYC")
):
    """
    Выполняет KYC-классификацию выбранных аккаунтов.
    """
    _print_header()
    accounts = [{ 'login': l } for l in logins]
    results = []
    for fn in (check_identity, check_business, check_payment, check_policies):
        accounts = asyncio.run(asyncio.gather(*[fn(acc) for acc in accounts]))
    for acc in accounts:
        typer.echo(f"{acc['login']} -> KYC: {acc.get('kyc_status')}")


@typer_app.command()
def pipeline():
    """
    Запускает полный LMNR pipeline через CLI.
    """
    _print_header()
    typer.secho("Запуск lmnr run facebook_pervobil_ideal...\n", fg=typer.colors.MAGENTA)
    import subprocess
    subprocess.run([
        "lmnr", "run", "facebook_pervobil_ideal", "--config", "settings.toml"
    ])


@typer_app.command()
def visualize_graph(output: Optional[str] = typer.Option("accounts_graph.png", help="Файл для сохранения графа")):
    """
    Генерирует графовую визуализацию пулa аккаунтов.
    """
    _print_header()
    asyncio.run(visualize(output))
    typer.secho(f"Граф сохранен в {output}", fg=typer.colors.GREEN)


@typer_app.command()
def report():
    """
    Выводит краткий отчет по results.csv.
    """
    _print_header()
    try:
        import csv
        with open('results.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                typer.echo(row)
    except FileNotFoundError:
        typer.secho("results.csv не найден. Запустите pipeline сначала.", fg=typer.colors.RED)


if __name__ == "__main__":
    typer_app()
