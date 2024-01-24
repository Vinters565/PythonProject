import os
import pandas as pd


def csv_reader(file_name):
    """Открывает и читает необходимый файл, а также возвращяет полученный результат.

    Args:
       file_name (str): Название файла для чтения

    Returns:
        list(list), list: Полученные данные из прочитанного файла; строчка с названиями столбцов
    """
    with open(file_name, encoding="utf-8-sig") as file:
        df = pd.read_csv(file_name)
        return df


def separate_data(data):
    data['year'] = data['published_at'].str.slice(stop=4)
    split_data = {year: vac.drop('year', axis=1).reset_index(drop=True) for year, vac in data.groupby('year')}
    return split_data


def create_directory(name_directory):
    """Создает директорию для хранения разделенных по годам файлов"""
    path = os.getcwd() + f'\{name_directory}'
    if os.path.exists(path):
        print(f'Директория {path} уже существует')
        return True
    try:
        os.mkdir(path)
    except OSError:
        print(f'Создать директорию {path} не удалось')
        return False
    print(f'Успешно создана директория {path}')
    return True


def create_files(data):
    """Создает csv файлы, где каждый файл хранит данные о вакансиях за один определенный год

    Args:
        data: Данные для записи в файлы
    """
    path = os.getcwd() + "\years\\"
    for year in data.items():
        year[1].to_csv(f'{path}{year[0]}_year.csv', encoding='utf-8', index=False)


def main():
    create_directory('years')
    data_frame = csv_reader('vacancies.csv')
    split_data = separate_data(data_frame)
    create_files(split_data)


if __name__ == "__main__":
    main()
