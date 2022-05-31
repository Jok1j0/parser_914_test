import tkinter
from tkinter import *
from PIL import ImageTk, Image
from io import BytesIO
import requests


def get_image(response, token):
    for item in response['data']['cryptoCurrencyList']:
        if item.get('symbol').lower() == token.lower() or item.get('name').lower() == token.lower():
            r = requests.get(url=f'https://s2.coinmarketcap.com/static/img/coins/64x64/{item.get("id")}.png')
            pil_image = Image.open(BytesIO(r.content))
            pil_image.save(BytesIO(), format="PNG")

            img = ImageTk.PhotoImage(pil_image)
            label1 = tkinter.Label(image=img)
            label1.image = img
            label1.place(x=300, y=110)


def get_data(token):
    response = requests.get(
        url=f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=200',
        stream=True
    ).json()
    rub = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()

    for item in response['data']['cryptoCurrencyList']:
        if item['symbol'].lower() == token.lower() or item['name'].lower() == token.lower():
            name = item['name']
            symbol = item['symbol']
            price = item['quotes'][0]['price']
            usd_rub = rub['Valute']['USD']['Value'] * round(price, 2)

            message = (
                f'Токен - {name} ({symbol})\n'
                f'Цена - {round(usd_rub, 2)} ₽RUB \ {round(price, 2)} $USD\n'
            )

            show_info.configure(text=message)
            get_image(response, token)


root = Tk()
root.geometry('666x333')
root.title('Парсинг криптовалют')
root.resizable(width=True, height=True)

start = Label(text='Введите название криптовалюты', font=("Arial", 14))
start.place(relx=.5, rely=.05, anchor="c")

show_info = Label(text='', font=("Arial", 12))
show_info.place(relx=.5, rely=.3, anchor="c")

message_entry = Entry()
message_entry.place(relx=.55, rely=.13, anchor="c")

btn = Button(root, text='search', command=lambda: get_data(message_entry.get()))
btn.place(relx=.4, rely=.13, anchor="c")

label = Label(root, compound='top')

root.mainloop()