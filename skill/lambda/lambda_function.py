from Model.Message import Message
from API.ListManager import ListManager
import requests
import logging
import boto3
import os

import ask_sdk_core.utils as ask_utils
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_dynamodb.adapter import user_id_partition_keygen


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "dummy"


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    message = Message()

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("Launh request intent triggered")

        return (
            handler_input.response_builder
            .speak(self.message.open())
            .ask(self.message.reprompt)
            .response
        )


class ConfigurationIntentHandler(AbstractRequestHandler):
    """Handler for Configuration Intent."""
    message = Message()

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ConfigurationIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Configuration intent triggered")

        chat_id = handler_input.request_envelope.request.intent.slots.get(
            "chat_id").value

        authority_chat_type = handler_input.request_envelope.request.intent.slots.get(
            "chat_type").resolutions.resolutions_per_authority

        group_type = False

        for x in authority_chat_type:
            for y in x.values:
                if y.value.name == "Group":
                    group_type = True
                    break
            else:
                continue
            break

        # configure group or single chat
        if group_type:
            chat_id = "-"+chat_id

        # save chat_id
        try:
            persistence_attr = handler_input.attributes_manager.persistent_attributes
            persistence_attr['chat_id'] = chat_id
            handler_input.attributes_manager.save_persistent_attributes()
        except Exception:
            logger.error(f"Configuration failed for chat_id \"{chat_id}\"")
            return (
                handler_input.response_builder
                .speak(self.message.configurationFailed())
                .set_should_end_session(True)
                .response
            )

        return (
            handler_input.response_builder
            .speak(self.message.configurationSuccess())
            .set_should_end_session(True)
            .response
        )


class SendShopListIntentHandler(AbstractRequestHandler):
    """Handler for Send Shop List Intent."""

    message = Message()

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SendShopListIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Send shop list intent triggered")
        response_builder = handler_input.response_builder

        # check for permission to read List
        request = handler_input.request_envelope

        if not (request.context.system.user.permissions and request.context.system.user.permissions.consent_token):
            response_builder.speak(
                "Non ho i permessi per leggere la lista, aggiungili dall'app Alexa nella sessione Skills")
            response_builder.set_card(AskForPermissionsConsentCard(
                permissions=["read::alexa:household:list"]))
        else:
            try:
                chat_id = handler_input.attributes_manager.persistent_attributes['chat_id']
            except KeyError as e:
                logger.error(e)
                return (
                    response_builder.
                    speak(self.message.errorChatIDNotSetted())
                    .ask(self.message.reprompt)
                    .response
                )

            try:
                l = ListManager(handler_input, "Alexa shopping list")
            except ValueError as e:
                logger.warning(e)
                return response_builder.speak(self.message.errorListNotFound("Spesa")).response

            itemsList = l.getListItem()

            if itemsList:
                s = "Lista *Spesa*:\n\n- "
                s += '\n- '.join(x['value'] for x in itemsList)
            else:
                s = "Lista *Spesa* vuota"

            s += "\n\nCondivisa dalla skill *List Manager* di Alexa"

            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            myobj = {'chat_id': chat_id, 'text': s, "parse_mode": "markdown"}
            x = requests.post(url, data=myobj)

            if (x.status_code == 200):
                response_builder.speak(self.message.sentList("Spesa"))
            else:
                response_builder.speak(self.message.errorTG())

        return response_builder.response


class SendToDoListIntentHandler(AbstractRequestHandler):
    """Handler for Send ToDo List Intent."""

    message = Message()

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SendToDoListIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Send to-do list intent triggered")
        response_builder = handler_input.response_builder

        # check for permission to read List
        request = handler_input.request_envelope

        if not (request.context.system.user.permissions and request.context.system.user.permissions.consent_token):
            response_builder.speak(
                "Non ho i permessi per leggere la lista, aggiungili dall'app Alexa nella sessione Skills")
            response_builder.set_card(AskForPermissionsConsentCard(
                permissions=["read::alexa:household:list"]))
        else:
            try:
                chat_id = handler_input.attributes_manager.persistent_attributes['chat_id']
            except KeyError as e:
                logger.error(e)
                return (
                    response_builder.
                    speak(self.message.errorChatIDNotSetted())
                    .ask(self.message.reprompt)
                    .response
                )

            try:
                l = ListManager(handler_input, "Alexa to-do list")
            except ValueError as e:
                logger.warning(e)
                return response_builder.speak(self.message.errorListNotFound("Cose da fare")).response

            itemsList = l.getListItem()

            if itemsList:
                s = "Lista *Cose da fare*:\n\n- "
                s += '\n- '.join(x['value'] for x in itemsList)
            else:
                s = "Lista *Cose da fare* vuota"

            s += "\n\nCondivisa dalla skill *List Manager* di Alexa"

            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            myobj = {'chat_id': chat_id, 'text': s, "parse_mode": "markdown"}
            x = requests.post(url, data=myobj)

            if (x.status_code == 200):
                response_builder.speak(
                    self.message.sentList("Cose da fare"))
            else:
                logger.error(f"Telegram error: {x}")
                response_builder.speak(self.message.errorTG())

        return response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    message = Message()

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Help intent triggered")

        return (
            handler_input.response_builder
            .speak(self.message.help())
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    message = Message()

    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("Cancel or stop intent triggered")

        return (
            handler_input.response_builder
            .speak(self.message.stop())
            .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    message = Message()

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("FallbackIntentHandler triggered")

        return (
            handler_input.response_builder
            .speak(self.message.fallback())
            .ask(self.message.reprompt)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    message = Message()

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        return (
            handler_input.response_builder
            .speak(self.message.error())
            .response
        )


ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')

ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
sb = StandardSkillBuilder(table_name=ddb_table_name, auto_create_table=False,
                          partition_keygen=user_id_partition_keygen, dynamodb_client=ddb_resource)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ConfigurationIntentHandler())
sb.add_request_handler(SendShopListIntentHandler())
sb.add_request_handler(SendToDoListIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
# sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

lambda_handler = sb.lambda_handler()
