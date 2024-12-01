import json
from zcatalyst_cliq.bot_handler import (
    welcome_handler,
    message_handler,
    context_handler,
    mention_handler,
    menu_action_handler,
    webhook_handler,
    participation_handler,
    BotWelcomeHandlerRequest,
    BotMessageHandlerRequest,
    BotContextHandlerRequest,
    BotMentionHandlerRequest,
    BotMenuActionHandlerRequest,
    BotParticipationHandlerRequest,
    BotWebHookHandlerRequest,
    HandlerResponse
)
from zcatalyst_sdk.catalyst_app import CatalystApp
import logging

@welcome_handler
def welcome_handler_fn(req: BotWelcomeHandlerRequest, res: HandlerResponse, *args):
    res.text = f'Hello {req.user.first_name}. Welcome to Zenkins! This extension seamlessly integrates Jenkins with Zoho Cliq, allowing you to easily manage nodes, jobs, and builds while visualizing everything at a glance.\nStart your journey by typing `explore` to explore Zenkins.'
    card = res.new_card()
    card.title = "Welcome to Zenkins"
    res.card = card
#     slide = res.new_slide()
#     slide.type = "text"
#     slide.data = """Zenkins is a Zoho Cliq extension that integrates Jenkins with Zoho Cliq, allowing users to manage and interact with Jenkins servers directly from within the Zoho Cliq interface. With Zenkins, users can seamlessly control their Jenkins environment through simple commands and interactive widgets, improving productivity and streamlining DevOps processes.

# Key Components of Zenkins:
# /connect Command:

# Establishes a connection between Zoho Cliq and a Jenkins server. This command allows users to authenticate and integrate Jenkins with Zoho Cliq.
# /disconnect Command:

# Disconnects from the Jenkins server, terminating the connection between Zoho Cliq and Jenkins.
# Widgets:

# System Info Widget: Displays detailed information about the Jenkins server's configuration, including system health and status.
# Jobs Widget: Lists and allows management of Jenkins jobs, including viewing job statuses, creating new jobs, and deleting existing ones.
# Builds Widget: Displays active, completed, and pending builds, including build logs and status updates.
# Nodes Widget: Provides information about the Jenkins nodes, showing their health and current status, and allowing management of nodes (e.g., creating or deleting nodes).
# Job Management:

# Create Job: Allows users to create new Jenkins jobs from within Zoho Cliq.
# Delete Job: Enables users to delete Jenkins jobs directly from Zoho Cliq.
# Build Management:

# Start Build: Provides a command to start a Jenkins build for any job directly from Zoho Cliq.
# Monitor Builds: Tracks the status of ongoing or completed builds, and allows users to view build logs.
# Node Management:

# Create Node: Facilitates the addition of new Jenkins nodes to the system.
# Delete Node: Allows users to remove Jenkins nodes as needed.
# """
#     res.add_slides(slide)
    return res


@message_handler
def msg_handler(req: BotMessageHandlerRequest, res: HandlerResponse, *args):
    try:
        msg = req.message
        text = ''
        if not msg:
            text = 'Please enable \'Message\' in bot settings'
        elif msg == 'hi' or msg == 'hello':
            text = f'Hi {req.user.first_name} :smile: . How are you doing ??'

            suggestions = res.new_suggestion_list()

            suggestions.add_suggestions(
                suggestions.new_suggestion('Good'),
                suggestions.new_suggestion('Not Bad'),
                suggestions.new_suggestion('meh'),
                suggestions.new_suggestion('Worst'),
            )
            res.suggestions = suggestions
        elif msg == 'Good' or msg == 'Not Bad':
            text = 'That\'s glad to hear :smile:'
        elif msg == 'meh' or msg == 'Worst':
            text = "Oops! Don't you worry. Your day is definitely going to get better. :grinning:"
        elif msg == "explore" or msg == "details":
            card = res.new_card()
            card.title = "Zenkins Guide"
            res.card = card
            text = 'Zenkins is a Zoho Cliq extension that integrates `Jenkins` with Zoho Cliq, allowing users to manage and interact with Jenkins servers directly from within the Zoho Cliq interface. With Zenkins, users can seamlessly control their Jenkins environment through simple commands and interactive widgets, improving productivity and streamlining DevOps processes.\n\n*Commands*\n1) `/connect`: Connects to the Jenkins Server.\n2) `/disconnect`: Disconnects the Jenkins Server. Use "/connect" to reconnect.\n3) `/getjobconfig`: Gets the Job configuration of an existing job.\n4) `/getnodeconfig`: Generates a Node configuration, which can be used in Node creation process.\n\n*Widgets*\n1) `System Info Tab`: Displays the Jenkins Server information\n2) `Jobs Tab`: Displays the information about each Job. Also allows us to "Create" and "Delete" jobs.\n3) `Builds Tab`: Displays the information about each Build. Also allows us to "Start" builds.\n4) `Nodes Tab`: Displays the information about each Node. Also allows us to "Create" and "Delete" nodes.\n\n*Resources*\n[Official Jenkins Website](https://www.jenkins.io/)\n[Jenkins on AWS](https://www.jenkins.io/doc/tutorials/tutorial-for-installing-jenkins-on-AWS/)\n[Guided Tutorial on Jenkins](https://www.jenkins.io/doc/pipeline/tour/getting-started/)'
            res.set_text(text)
        else:
            text = "Oops! Sorry, I'm not sure about that.\n Type `explore` to learn more about Zenkins."
        res.set_text(text)
        return res
    except Exception as e:
        logging.error(e)
        return
    
@context_handler
def ctx_handler(req: BotContextHandlerRequest, res: HandlerResponse, *args):
    return res


@mention_handler
def mention_handler(req: BotMentionHandlerRequest, res: HandlerResponse, *args):
    return res


@menu_action_handler
def action(req: BotMenuActionHandlerRequest, res: HandlerResponse, *args):
    return res


@participation_handler
def participation(req: BotParticipationHandlerRequest, res: HandlerResponse, *args):
    return res

@webhook_handler
def webhook_fn(req: BotWebHookHandlerRequest, res: HandlerResponse, *args):
    return res
