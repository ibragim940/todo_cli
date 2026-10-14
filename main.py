
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"


def load_tasks() -> list[dict]:
    """Загрузить задачи из JSON-файла."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)

        if not isinstance(tasks, list):
            print("Ошибка: файл задач должен содержать список.")
            return []

        return tasks

    except (json.JSONDecodeError, OSError) as error:
        print(f"Не удалось загрузить задачи: {error}")
        return []


def save_tasks(tasks: list[dict]) -> None:
    """Сохранить задачи в JSON-файл."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)

    except OSError as error:
        print(f"Не удалось сохранить задачи: {error}")


def show_tasks(tasks: list[dict]) -> None:
    """Показать все задачи."""
    if not tasks:
        print("\nСписок задач пуст.")
        return

    print("\n=== СПИСОК ЗАДАЧ ===")

    for index, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else " "
        print(f"{index}. [{status}] {task['title']}")


def add_task(tasks: list[dict]) -> None:
    """Добавить новую задачу."""
    title = input("Введите название задачи: ").strip()

    if not title:
        print("Название задачи не может быть пустым.")
        return

    task = {
        "title": title,
        "done": False,
    }

    tasks.append(task)
    save_tasks(tasks)

    print("Задача успешно добавлена.")


def complete_task(tasks: list[dict]) -> None:
    """Отметить задачу как выполненную."""
    show_tasks(tasks)

    if not tasks:
        return

    try:
        number = int(input("Номер выполненной задачи: "))
    except ValueError:
        print("Введите целое число.")
        return

    if not 1 <= number <= len(tasks):
        print("Задачи с таким номером нет.")
        return

    task = tasks[number - 1]

    if task["done"]:
        print("Эта задача уже выполнена.")
        return

    task["done"] = True
    save_tasks(tasks)

    print("Задача отмечена как выполненная.")


def delete_task(tasks: list[dict]) -> None:
    """Удалить задачу."""
    show_tasks(tasks)

    if not tasks:
        return

    try:
        number = int(input("Номер задачи для удаления: "))
    except ValueError:
        print("Введите целое число.")
        return

    if not 1 <= number <= len(tasks):
        print("Задачи с таким номером нет.")
        return

    removed_task = tasks.pop(number - 1)
    save_tasks(tasks)

    print(f"Задача «{removed_task['title']}» удалена.")


def show_menu() -> None:
    """Показать меню программы."""
    print("\n=== TODO MANAGER ===")
    print("1. Показать задачи")
    print("2. Добавить задачу")
    print("3. Выполнить задачу")
    print("4. Удалить задачу")
    print("0. Выход")


def main() -> None:
    """Главная функция программы."""
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_tasks(tasks)

        elif choice == "2":
            add_task(tasks)

        elif choice == "3":
            complete_task(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "0":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()
