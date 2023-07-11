import json
import re
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Загружаем файл JSON
with open('/Users/mikhail/Desktop/Code/work_with_chat/result.json', 'r') as f:
    data = json.load(f)

# Описываем в RegExp слово, которое будем искать
pattern = re.compile(r'(П|п)ив(о|а|ы)', re.IGNORECASE)

# Создаем переменные для временных периодов
morning_period = list(range(4, 12))  # с 4:00 до 12:00
day_period = list(range(12, 17))  # с 12:00 до 17:00
evening_period = range(17, 24)  # с 17:00 до 00:00
night_period = list(range(0, 5))  # с 00:00 до 5:00

# Ищем сообщения, которые содержат искомое слово и разделяем их по времени суток
morning_messages=[]
day_messages=[]
evening_messages=[]
night_messages=[]

for message in data['messages']:
    if 'text' in message:
        if isinstance(message['text'], list):
            # Здесь мы собираем список строк в единую строку
            text=' '.join(str(x) for x in message['text'])
        else:
            text=message['text']
        match=pattern.search(text)
        if match:
            # Выделяем часы из времени сообщения
            date_string=message['date']
            date=datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
            hour=date.hour

            # Разделяем сообщения по времени суток
            if hour in morning_period:
                morning_messages.append(message)
            elif hour in day_period:
                day_messages.append(message)
            elif hour in evening_period:
                evening_messages.append(message)
            elif hour in night_period:
                night_messages.append(message)

# Выводим колличество сообщений для каждого времени суток
print("Количество сообщений содержащих упоминание пива по времени суток")
print("Утро:", len(morning_messages))
print("День:", len(day_messages))
print("Вечер:", len(evening_messages))
print("Ночь:", len(night_messages))

# Создаем диаграмму, в которой визуализируем частоту сообщений по времени суток
labels=['Утро', 'День', 'Вечер', 'Ночь']
values=[len(morning_messages), len(day_messages),
            len(evening_messages), len(night_messages)]

plt.bar(labels, values)
plt.title('Количество сообщений содержащих упоминание пива по времени суток')
plt.xlabel('Время суток')
plt.ylabel('Количество сообщений')
plt.show()