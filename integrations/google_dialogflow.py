from google.cloud import dialogflow
import logging


def get_agent_answer(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    logger = logging.getLogger("DialogBot.GoogleRequest")
    logger.debug('Session path: {}\n'.format(session))

    text_input = dialogflow.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(
            request={'session': session, 'query_input': query_input})
        logger.info('Make request to google DialogFlow')
    except ConnectionError as er:
        logger.exception(er)
    except Exception as er:
        logging.exception(er)

    return response.query_result
