import dialogflow_v2
import requests
import environ
import dialogflow_v2beta1
import logging

logger = logging.getLogger("DialogBot.GoogleRequest")
logger.debug('Session path: {}\n'.format(session))

def get_intent_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def put_intent(intent, project_id):
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(project_id)
    response = client.create_intent(parent, intent)
    logger.debug(response)


def transform_question_category(question_category):
    intent = {'display_name': question_category[0], 'messages': []}
    intent['messages'].append({'text': {'text': [question_category[1]['answer']]}})
    intent['training_phrases'] = [{'parts': [{'text': question}]}
                                  for question in question_category[1]['questions']]
    return intent


def train_agent(project_id):
    client = dialogflow_v2beta1.AgentsClient()
    parent = client.project_path(project_id)
    response = client.train_agent(parent)
    logger.debug(response)


if __name__ == "__main__":
    env = environ.Env()
    env.read_env()
    logger = logging.getLogger("DialogBot.TrainAgent")
    project_id = env('GOOGLE_PROJECT_ID')
    url = env('QUESTIONS_URL')
    questions = get_intent_text(url)
    for i in questions.items():
        data = transform_question_category(i)
        try:
            put_intent(data, project_id)
        except:
            continue
    train_agent(project_id)
