import zcatalyst_cliq
import zcatalyst_sdk
config = {
    "ZohoCliq": {
        "handlers": {
            "bot_handler": "handlers/bot_handler.py",
            "function_handler": "handlers/function_handler.py",
            # "installation_validator": "handlers/installation_validator.py",
            "command_handler": "handlers/command_handler.py",
            "widget_handler": "handlers/widget_handler.py",
            # "messageaction_handler": "handlers/message_action_handler.py",
            # "installation_handler": "handlers/installation_handler.py"
        }
    },
}


def handler(request, response):
    catalyst_app = zcatalyst_sdk.initialize("test")
    handler_resp = zcatalyst_cliq.execute(request, config)
    response.set_content_type('application/json')
    response.send(handler_resp)
