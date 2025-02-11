import httpx
import json
from rich.table import Table
from rich.console import Console
from logger import log_info, log_error  # Импорт логирования

API_URL = "http://127.0.0.1:8000/api"  # Адрес API сервера
console = Console()


def fetch_resources():
    """Получает список ресурсов с сервера"""
    try:
        response = httpx.get(f"{API_URL}/resources")
        response.raise_for_status()
        data = response.json()
        log_info(f"Успешный запрос /resources: {data}")
        return data
    except httpx.HTTPStatusError as e:
        console.print(f"[red]Ошибка запроса: {e.response.status_code}[/red]")
        log_error(f"Ошибка запроса /resources: {e.response.status_code}")
        return []
    except Exception as e:
        console.print(f"[red]Ошибка соединения: {e}[/red]")
        log_error(f"Ошибка соединения: {e}")
        return []


def display_resources(resources):
    """Выводит список ресурсов в виде таблицы"""
    if not resources:
        console.print("[yellow]Нет данных о ресурсах.[/yellow]")
        return

    table = Table(title="Рынок ресурсов")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Название", style="green")
    table.add_column("Количество", justify="right", style="yellow")
    table.add_column("Цена", justify="right", style="magenta")

    for res in resources:
        table.add_row(str(res["id"]), res["name"], str(res["quantity"]), str(res["price"]))

    console.print(table)


def buy_resource(resource_id, amount):
    """Покупает ресурс"""
    try:
        payload = {"quantity": amount}
        response = httpx.post(f"{API_URL}/buy/{resource_id}", json=payload)
        response.raise_for_status()
        console.print(f"[green]Успешно куплено {amount} единиц ресурса {resource_id}[/green]")
        log_info(f"Покупка ресурса {resource_id}, количество: {amount}, ответ сервера: {response.json()}")
    except httpx.HTTPStatusError as e:
        console.print(f"[red]Ошибка при покупке: {e.response.json()}[/red]")
        log_error(f"Ошибка при покупке ресурса {resource_id}: {e.response.json()}")
    except Exception as e:
        console.print(f"[red]Ошибка соединения: {e}[/red]")
        log_error(f"Ошибка соединения при покупке ресурса {resource_id}: {e}")


def main():
    """Главное меню"""
    while True:
        console.print("\n[bold cyan]MarketMind CLI[/bold cyan]")
        console.print("1. Посмотреть ресурсы\n2. Купить ресурс\n3. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            resources = fetch_resources()
            display_resources(resources)

        elif choice == "2":
            try:
                resource_id = int(input("Введите ID ресурса: "))
                amount = int(input("Введите количество: "))
                buy_resource(resource_id, amount)
            except ValueError:
                console.print("[red]Ошибка: введите числовые значения![/red]")
                log_error("Ошибка: введены некорректные данные для ID или количества.")

        elif choice == "3":
            console.print("[bold red]Выход...[/bold red]")
            log_info("Клиент завершил работу.")
            break

        else:
            console.print("[red]Неверный ввод, попробуйте снова.[/red]")
            log_error("Пользователь ввел некорректный пункт меню.")


if __name__ == "__main__":
    log_info("Клиент запущен.")
    main()
