from datetime import datetime

class Record:
    """
    Класс Record представляет собой запись о доходе или расходе.
    Содержит поля: date (дата), category (категория: Доход или Расход), amount (сумма) и description (описание).
    """
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

class FinanceTracker:
    """
    Класс FinanceTracker управляет финансовыми записями.
    Содержит методы для загрузки и сохранения данных, добавления, редактирования, удаления и поиска записей, а также показа баланса.
    """
    def __init__(self, data_file):
        # data_file - путь к текстовому файлу для хранения записей
        self.data_file = data_file
        # Инициализируем пустой список для хранения записей
        self.records = []
        # Загружаем данные из файла при инициализации
        self.load_data()

    def load_data(self):
        """
        Загружает данные из текстового файла и преобразует их в список записей.
        """
        try:
            # Открываем файл для чтения
            with open(self.data_file, 'r') as file:
                record = None
                # Читаем файл построчно
                for line in file:
                    line = line.strip()
                    # Если строка начинается с 'Дата:', начинаем новую запись
                    if line.startswith('Дата:'):
                        # Если уже есть текущая запись, добавляем ее в список
                        if record:
                            self.records.append(record)
                        # Создаем новую запись
                        record = Record(line.split(': ')[1], '', 0, '')
                    elif line.startswith('Категория:'):
                        # Устанавливаем категорию записи
                        record.category = line.split(': ')[1]
                    elif line.startswith('Сумма:'):
                        # Устанавливаем сумму записи
                        record.amount = float(line.split(': ')[1])
                    elif line.startswith('Описание:'):
                        # Устанавливаем описание записи
                        record.description = line.split(': ')[1]
                # Добавляем последнюю запись в список, если она существует
                if record:
                    self.records.append(record)
        except FileNotFoundError:
            # Если файл не найден, просто продолжаем, считая, что нет данных для загрузки
            pass

    def save_data(self):
        """
        Сохраняет данные в текстовый файл в соответствии с форматом.
        """
        with open(self.data_file, 'w') as file:
            # Сохраняем каждую запись из списка в файл
            for record in self.records:
                file.write(f'Дата: {record.date}\n')
                file.write(f'Категория: {record.category}\n')
                file.write(f'Сумма: {record.amount}\n')
                file.write(f'Описание: {record.description}\n')
                # Добавляем пустую строку между записями для разделения
                file.write('\n')

    def add_record(self, date, category, amount, description):
        """
        Добавляет новую запись о доходе или расходе.
        """
        # Создаем новую запись и добавляем ее в список
        record = Record(date, category, amount, description)
        self.records.append(record)
        # Сохраняем данные в файл
        self.save_data()

    def edit_record(self, index, date, category, amount, description):
        """
        Редактирует существующую запись по индексу.
        """
        # Проверяем, что индекс находится в пределах допустимого диапазона
        if index < 0 or index >= len(self.records):
            print('Некорректный индекс записи.')
            return
        # Обновляем запись по указанному индексу
        self.records[index] = Record(date, category, amount, description)
        # Сохраняем данные в файл
        self.save_data()

    def delete_record(self, index):
        """
        Удаляет запись по индексу.
        """
        # Проверяем, что индекс находится в пределах допустимого диапазона
        if index < 0 or index >= len(self.records):
            print('Некорректный индекс записи.')
            return
        # Удаляем запись по индексу
        del self.records[index]
        # Сохраняем данные в файл
        self.save_data()

    def search_records(self, query):
        """
        Ищет записи по категории, дате, сумме или описанию.
        """
        # Перебираем все записи
        for i, record in enumerate(self.records):
            # Если запрос содержится в какой-либо части записи, выводим ее
            if query in record.date or query in record.category or str(record.amount) == query:
                print(f'{i}: Дата: {record.date}, Категория: {record.category}, Сумма: {record.amount}, Описание: {record.description}')

    def show_balance(self):
        """
        Показывает текущий баланс, общий доход и общий расход.
        """
        # Суммируем доходы и расходы
        income = sum(record.amount for record in self.records if record.category == 'Доход')
        expense = sum(record.amount for record in self.records if record.category == 'Расход')
        # Вычисляем баланс
        balance = income - expense
        # Выводим баланс, общий доход и общий расход
        print(f'Текущий баланс: {balance}')
        print(f'Общий доход: {income}')
        print(f'Общий расход: {expense}')

    def is_valid_date(self, date_string):
        """
        Проверяет, является ли строка корректной датой в формате "гггг-мм-дд".
        """
        try:
            # Пытаемся преобразовать строку в дату
            parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            # Если преобразование не удалось, возвращаем False
            return False

def main():
    # Указываем путь к файлу данных
    data_file = 'data.txt'
    # Создаем объект FinanceTracker для управления записями
    tracker = FinanceTracker(data_file)

    while True:
        # Выводим меню
        print('--- Меню ---')
        print('1. Добавить запись')
        print('2. Редактировать запись')
        print('3. Удалить запись')
        print('4. Поиск записей')
        print('5. Показать баланс')
        print('6. Выйти')
        # Читаем выбор пользователя
        choice = input('Введите ваш выбор: ')

        # Добавление новой записи
        if choice == '1':
            date = input('Введите дату (гггг-мм-дд): ')
            # Проверка корректности введенной даты
            while tracker.is_valid_date(date) == False:
                date = input('Введите дату (гггг-мм-дд): ')
            # Ввод категории
            category = input('Введите категорию (Доход/Расход): ')
            # Проверка корректности введенной категории
            while category != 'Доход' and category != 'Расход':
                category = input('Введите категорию (Доход/Расход): ')
            # Ввод суммы и проверка, что сумма не отрицательна
            amount = float(input('Введите сумму: '))
            while amount < 0:
                amount = float(input('Введите сумму: '))
            # Ввод описания
            description = input('Введите описание: ')
            # Добавляем новую запись
            tracker.add_record(date, category, amount, description)

        # Редактирование существующей записи
        elif choice == '2':
            index = int(input('Введите индекс записи для редактирования: '))
            date = input('Введите новую дату (гггг-мм-дд): ')
            # Проверка корректности введенной даты
            while tracker.is_valid_date(date) == False:
                date = input('Введите дату (гггг-мм-дд): ')
            category = input('Введите новую категорию (Доход/Расход): ')
            # Проверка корректности введенной категории
            while category != 'Доход' and category != 'Расход':
                category = input('Введите категорию (Доход/Расход): ')
            # Ввод новой суммы и проверка, что сумма не отрицательна
            amount = float(input('Введите новую сумму: '))
            while amount < 0:
                amount = float(input('Введите сумму: '))
            description = input('Введите новое описание: ')
            # Редактируем запись
            tracker.edit_record(index, date, category, amount, description)

        # Удаление существующей записи
        elif choice == '3':
            index = int(input('Введите индекс записи для удаления: '))
            # Удаляем запись
            tracker.delete_record(index)

        # Поиск записей
        elif choice == '4':
            query = input('Введите строку для поиска: ')
            # Ищем записи по запросу
            tracker.search_records(query)

        # Показ баланса
        elif choice == '5':
            # Показываем баланс, доход и расход
            tracker.show_balance()

        # Выход из программы
        elif choice == '6':
            break
        else:
            print('Некорректный выбор, попробуйте снова.')

if __name__ == '__main__':
    main()
