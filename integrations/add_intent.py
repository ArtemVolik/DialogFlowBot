import dialogflow_v2
import requests
from environs import Env
import dialogflow_v2beta1
from logs.logging_maintenace import get_logger_from_config


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def put_intent(intent, project_id):
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(project_id)
    response = client.create_intent(parent, intent)
    logger.debug(response)


def transform_question_category(row):
    question_category, content = row
    answer = content['answer']
    questions = content['questions']
    intent = {'display_name': question_category, 'messages': []}
    intent['messages'].append({'text': {'text': [answer]}})
    intent['training_phrases'] = [{'parts': [{'text': question}]}
                                  for question in questions]
    return intent


def train_agent(project_id):
    client = dialogflow_v2beta1.AgentsClient()
    parent = client.project_path(project_id)
    response = client.train_agent(parent)
    logger.debug(response)


if __name__ == "__main__":
    env = Env()
    Env.read_env()
    logger = get_logger_from_config('logs/log_config.yaml', env('NOTIFICATION_TOKEN'), env('NOTIFICATION_CHAT_ID'),
                                    "DialogBot.TrainAgent")
    project_id = env('GOOGLE_PROJECT_ID')
    url = env('QUESTIONS_URL')
    questions = get_intent_text(url)
    for i in questions.items():
        data = transform_question_category(i)
        try:
            put_intent(data, project_id)
        except ConnectionError:
            continue
    train_agent(project_id)
