import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

print("Этап 1. Анализ данных")
print("-" * 50)

# Загрузка данных из JSON файла
try:
    with open('events.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    df = pd.DataFrame(data["events"])

    print(f"Данные успешно загружены. Размер датафрейма: {df.shape}")
    print(f"Количество записей: {len(df)}")
    print(f"Колонки: {df.columns.tolist()}")

    # Анализ распределения событий по типам
    print("\nАнализ распределения событий по типам (signature):")

    # Подсчет количества событий каждого типа
    signature_counts = df['signature'].value_counts()

    print(f"Всего уникальных типов событий: {len(signature_counts)}")
    print(f"\nРаспределение по типам:")
    for signature, count in signature_counts.items():
        print(f"  {signature}: {count}")

    print(f"\nОбщее количество событий: {signature_counts.sum()}")

    #Визуализация данных
    print("\n" + "=" * 50)
    print("Этап 2. Визуализация данных")
    print("-" * 50)

    # Создание графика
    plt.figure(figsize=(12, 8))

    ax = sns.countplot(data=df, y="signature", order=df['signature'].value_counts().index)

    # Настройка графика
    plt.title("Распределение типов событий информационной безопасности",
              fontsize=14, fontweight='bold')
    plt.xlabel("Количество событий", fontsize=12)
    plt.ylabel("Тип события", fontsize=12)

    # Добавление значений на столбцы
    for i, v in enumerate(df['signature'].value_counts().values):
        ax.text(v + 0.5, i, str(v), va='center', fontsize=10)

    # Настройка сетки для лучшей читаемости
    plt.grid(axis='x', alpha=0.3)

    # Сохранение графика
    plt.tight_layout()
    plt.savefig('events_distribution.png', dpi=100, bbox_inches='tight')
    print("График сохранен в файл 'events_distribution.png'")

    # Отображение графика
    plt.show()

    # Дополнительная статистика
    print("\n" + "=" * 50)
    print("Дополнительная статистика:")
    print(f"Максимальное количество событий одного типа: {signature_counts.max()}")
    print(f"Минимальное количество событий одного типа: {signature_counts.min()}")
    print(f"Среднее количество событий на тип: {signature_counts.mean():.2f}")
    print(f"Медианное количество событий на тип: {signature_counts.median():.2f}")

    # Анализ по категориям (первые слова в signature)
    print("\nАнализ по основным категориям:")
    categories = {}
    for sig in df['signature'].unique():
        category = sig.split()[0]  # Берем первое слово как категорию
        if category in categories:
            categories[category] += signature_counts[sig]
        else:
            categories[category] = signature_counts[sig]

    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count} событий")

    print("\nАнализ завершен успешно!")

except FileNotFoundError:
    print("Ошибка: Файл 'events.json' не найден в текущей директории!")
    print("Пожалуйста, убедитесь, что файл с данными находится в той же папке, что и скрипт.")
except KeyError as e:
    print(f"Ошибка: В JSON файле отсутствует ключ 'events' - {e}")
    print("Проверьте структуру JSON файла.")
except json.JSONDecodeError:
    print("Ошибка: Файл не является корректным JSON!")
except Exception as e:
    print(f"Произошла ошибка: {e}")