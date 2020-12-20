# Умный Telegram/VK bot + Google DialogFlow
2 бота сделаны в учебно-тренировочных целях.
Скрипт, по сути, является посредником между пользовательским интерфейсом VK/Telegram и
умным роботом от гугла. При правильном подходе к подготовке контента и обучению бота DialogFlow, 
можно автоматизировать рутинные переписки с клиентами, например. Ну или организовать альтернативу 
"сексу по телефону", извращенцев хватает.  
[тестовый телеграм-бот](https://t.me/vasiliy_publishing_bot?start)  
[тестовый паблик Вк](https://vk.com/public201158246)

Выглядит это так:  
![Alt text](/Screenshot_vk.png?raw=true "VK")  
![Alt text](/Screenshot_tg.png?raw=true "telegram")

## Установка  
 
### Предварительно: 
- создать [телеграм-бота](https://telegram.me/BotFather)
- создать проект [DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup)
- создать агента для [DialogFlow проекта](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)
- получить **google application credentials**
- получить токен для управления группой вконтакте, с правами на отправку сообщений.
- узнать собственный id в телеграмме (написать боту `@userinfobot` сообщение `\start`)

### Локальная установка
- Скопируйте все
- В корне проекта создайте файл **.env** и поместите в него следующее:  
  путь к файлу json  
```GOOGLE_APPLICATION_CREDENTIALS='/google_application_credentials.json'```  
  токен от телеграм бота  
```TELEGRAM_TOKEN='your_token'```  
  id вашего DialogFlow проекта (выглядит так: `dialogflowbot-111111`)  
```GOOGLE_PROJECT_ID='dialog_flow_project_id'```  
  токен вашей группы из управления сообществом  
  ```VK_API_KEY='vk_group_token'```  
для русскоязычного бота скопировать без изменений  
```LANGUAGE_CODE='RU'```  
  токен бота-нотификатора, можно использовать то же что выше или создать еще одного бота  
```NOTIFICATION_TOKEN='your_same_or_another_token'```  
  ваш id из telegram   
```NOTIFICATION_CHAT_ID='chat_id'```

        
- Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки 
зависимостей:  
    `pip install -r requirements.txt`

#### Проблемы:
У меня так и не получилось запустить ВК-бота локально в Украине через прокси специально приобретенные для этого.
Потому пришлось ставить VPN.


## Деплой Heroku:
Самый легкий способ, сделать аккаунт Heroku и связать его с вашим GitHub.
- Переменные окружения из `.env` перенести в [настройки Heroku](https://prnt.sc/vnv8w9)
- Для того чтобы подружить ваш деплой на Heroku c google выполните [указанные шаги](https://stackoverflow.com/questions/47446480/how-to-use-google-api-credentials-json-on-heroku)

## Скрипт для обучения робота
Агента DialogFlow можно обучать, для этого напиcан скрипт `add_intent.py`
Который данные из такого вот формата, ([пример](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json))
загружает  `intent` вашего агента и автоматически инициализирует обучение.
