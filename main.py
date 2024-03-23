import asyncio


# Функция для покупки подарка
async def buy_gift(gift):
    print(f"buy {gift}")
    await asyncio.sleep(gift["time_for_purchase"])
    print(f"got {gift['name']}")


# Функция для покупки подарков на каждой остановке
async def buy_gifts_at_stop(stop_number, gifts):
    print(f"buying gifts at {stop_number} stop")

    # Сортируем подарки в порядке уменьшения времени на покупку
    sorted_gifts = sorted(gifts, key=lambda x: x["time_for_purchase"])

    for gift in sorted_gifts:
        # Если есть достаточно времени на покупку, то покупаем подарок
        if gift["time_for_selection"] <= time_until_departure:
            await buy_gift(gift)

    print(f"arrive from {stop_number} stop")


# Считываем входные данные
stops_data = []
gifts_data = []

# Считываем информацию о каждой остановке
flag = True
while flag:
    try:
        departure_time, travel_duration = map(int, input().split())
        stops_data.append({"departure_time": departure_time, "travel_duration": travel_duration})
    except ValueError:
        flag = False
        break

# Считываем информацию о каждом подарке
flag = True
while flag:
    try:
        gift_name, time_for_selection, time_for_purchase = input().split()
        gifts_data.append({"name": gift_name, "time_for_selection": int(time_for_selection) / 100,
                           "time_for_purchase": int(time_for_purchase) / 100})
    except ValueError:
        flag = False
        break

# Инициализация переменных
time_until_departure = stops_data[0]["departure_time"]

# Создаем цикл событий asyncio
loop = asyncio.get_event_loop()

# Асинхронно покупаем подарки на каждой остановке
for stop_number, stop_data in enumerate(stops_data):
    if stop_number > 0:
        loop.run_until_complete(buy_gifts_at_stop(stop_number, gifts_data))

    time_until_departure -= stop_data["travel_duration"]

# Если остались не купленные подарки в пути, то покупаем их по прибытии
if gifts_data:
    print("buying gifts after arrival")
    for gift in gifts_data:
        loop.run_until_complete(buy_gift(gift))

# Закрываем цикл событий asyncio
loop.close()
