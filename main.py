import telebot
import requests
from datetime import datetime

from keyboards import HELO_BOARD
from telebot.types import Message, CallbackQuery
from settings import TOKEN, SOURCES


tasks = {}

def get_orgs(url, key):

    data = {
        'filters':  {
            "inn": key,
            'member_status': 1, 
            'sro_enabled': True
        }, 
        'page': 1, 
        'pageCount': "100", 
        'sortBy': {}, 
        'searchString': key
    }
    
    try:
        result = requests.post(url, json=data, timeout=5)
        return result.json()["data"]["data"]
    except:
        return []


def process_results(data):
    orgs = {}
    result = ''
    for org in data:
        print(orgs)
        if org["inn"] not in orgs:
            orgs[org["inn"]] = [org]
        else:
            orgs[org["inn"]].append(org)
    
    for inn in orgs:
        print(orgs[inn])
        result += "\n\n"
        # for item in orgs[inn]:
        #     item['last_updated'] = datetime.strptime(
        #         item['last_updated_at_date_time_string'],
        #         "%d.%m.%Y %H:%M:%S"
        #     )
        # orgs[inn].sort(key=lambda x: x['last_updated'])
        result += orgs[inn][0]['short_description']
        result += "\nИНН: " + orgs[inn][0]['inn']
        result += "\nОГРН: " + orgs[inn][0]['ogrnip']
        result += "\n" + orgs[inn][0]['director']
        result += "\nМестонахождение: " + orgs[inn][0]['region_number']['title']
        result += "\nАктивное членство в следующих СРО:"
        for item in orgs[inn]:
            sro = item['sro']['full_description']
            result += f"\n[👉 {sro}]({item['detail_url']})"
    return result


def serch_org(search_string):
    results = []
    for source in SOURCES:
        tmp = get_orgs(source["search_url"], search_string)
        for item in tmp:
            item['detail_url'] = source["detail_url_page"].format(item["id"])
        results += tmp
            

    result = process_results(results)
    print(result)
    if result:
        text = "По данному критерию найдено следующее:" + result
    else:
        text = "Ничего не найдено, попробуйте изменить запрос"
    return text
    

def get_detail(url_teplate, org_id):
    url = url_teplate.format(org_id)
    result = requests.post(url)
    return result.json()


if __name__ == "__main__":
    bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN")


    @bot.message_handler(commands=['start'])
    def start_message(message: Message):
        text = "Здравствуйте!"
        text += "\nДанный бот предназначен для работы с личным кабинетом ..."
        
        bot.send_message(
            chat_id=message.chat.id, 
            text=text,
            reply_markup=HELO_BOARD
        )
    

    @bot.message_handler(content_types='text')
    def process_text(message:Message): 
        state = tasks.get(message.chat.id)
        print(state)
        if message.text == "Поиск организации":
            tasks[message.chat.id] = {"state": "search"}
            text = "\nЗдесь Вы можете получить общедоступную информацию об организациях членах различных СРО"
            text += "\n\nПоиск осуществляется по ИНН"
            text += "\nОтправьте сообщение, поиск будет произведен по его содержимому"

        elif state and state["state"] == "search":
            try:
                text = serch_org(message.text)
            except:
                text = "Что то пошло не так... Попробуйте позже"
            tasks.__delitem__(message.chat.id)


        elif message.text == "Личный кабинет":
            text = "Данный функционал в разработке"
        
        else:
            text = "Выберите действие с помощью клавиатуры"

        bot.send_message(
            chat_id=message.chat.id, 
            text=text
        )

    bot.infinity_polling()