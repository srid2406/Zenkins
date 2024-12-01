from typing import List
import zcatalyst_cliq.command_handler as command
from zcatalyst_cliq.command_handler import (
    execution_handler,
    suggestion_handler,
    CommandHandlerRequest,
    CommandSuggestion,
    HandlerResponse,
)
import zcatalyst_sdk
from ujenkins import JenkinsClient

@execution_handler
def executor(req: CommandHandlerRequest, res: HandlerResponse, *args):
    text = ''
    cmd = req.name
    # if cmd == 'catalyst':
    #     suggestions = req.selections
    #     if not suggestions:
    #         text = 'Please select a suggestion from the command'
    #     else:
    #         prefix = 'Take a look at our '
    #         if suggestions[0].title == 'API doc':
    #             text = prefix + '[API Documentation](https://www.zoho.com/catalyst/help/api/introduction/overview.html)'
    #         elif suggestions[0].title == 'CLI doc':
    #             text = prefix + '[CLI Documentation](https://www.zoho.com/catalyst/help/cli-command-reference.html)'
    #         else:
    #             text = prefix + '[help documentation](https://www.zoho.com/catalyst/help/)'
    if cmd == 'connect':
        return get_form()
    if cmd == "disconnect":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            msg = command.new_handler_response().new_message()
            msg.text = 'No Jenkins Server Connected'
            msg.type = 'banner'
            msg.status = 'success'
            return msg
        else:
            try:
                client = JenkinsClient(url, username, apiKey)
                client.close()

                segment_service.delete(req.user.id+"url")
                segment_service.delete(req.user.id+"username")
                segment_service.delete(req.user.id+"apikey")
                msg = command.new_handler_response().new_message()
                msg.text = 'Disconnected Successfully. Use "/connect" to reconnect.'
                msg.type = 'banner'
                msg.status = 'success'
                return msg
            except Exception as e:
                msg = command.new_handler_response().new_message()
                msg.text = 'Failed to Disconnect. Try again.'
                msg.type = 'banner'
                msg.status = 'failure'
                return msg
    if cmd == "getjobconfig":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")

        client = JenkinsClient(url, username, apiKey)
        jobs = client.jobs.get()
        job_names = [job_info['name'] for job_info in jobs.values()]
        return get_form2(job_names)
    if cmd == "getnodeconfig":
        return get_form3()
    # elif cmd == "getjobconfig":
    #     app = zcatalyst_sdk.get_app("test")
    #     cache_service = app.cache()
    #     segment_service = cache_service.segment()
    #     url = segment_service.get_value(req.user.id+"url")
    #     username = segment_service.get_value(req.user.id+"username")
    #     apiKey = segment_service.get_value(req.user.id+"apikey")

    #     client = JenkinsClient(url, username, apiKey)
    #     jobs = client.jobs.get()
    #     job_names = [job_info['name'] for job_info in jobs.values()]
    #     return get_form2(job_names)
    # elif cmd == 'createjob':
    #     return form2()
    # elif cmd == "deletejob":
    #     app = zcatalyst_sdk.get_app("test")
    #     cache_service = app.cache()
    #     segment_service = cache_service.segment()
    #     url = segment_service.get_value(req.user.id+"url")
    #     username = segment_service.get_value(req.user.id+"username")
    #     apiKey = segment_service.get_value(req.user.id+"apikey")

    #     client = JenkinsClient(url, username, apiKey)
    #     jobs = client.jobs.get()
    #     job_names = [job_info['name'] for job_info in jobs.values()]
    #     return form4(job_names)
    # elif cmd == 'getjobs':
    #     app = zcatalyst_sdk.get_app("test")
    #     cache_service = app.cache()
    #     segment_service = cache_service.segment()
    #     url = segment_service.get_value(req.user.id+"url")
    #     username = segment_service.get_value(req.user.id+"username")
    #     apiKey = segment_service.get_value(req.user.id+"apikey")
    #     if not (url and username and apiKey) :
    #         text = "No active Jenkins connection. Please use the `connect` command first."
    #     else:
    #         try:
    #             client = JenkinsClient(url, username, apiKey)
    #             jobs = client.jobs.get()
    #             text = 'List of all Jobs'
    #             res.set_text(text)

    #             if jobs:
    #                 table_rows = []  # Store rows for the table
    #                 for job_name, job_info in jobs.items():
    #                     name = job_info.get('name', 'N/A')
    #                     url = job_info.get('url', 'N/A')
    #                     color = job_info.get('color', 'N/A')
    #                     project_type = job_info.get('_class', 'N/A')

    #                     if color == "blue":
    #                         final_color = " 🔵 "
    #                         final_status = "Success"
    #                     elif color == "notbuilt":
    #                         final_color = " ⚪ "
    #                         final_status = "Not Built"
    #                     elif color == "red":
    #                         final_color = " 🔴 "
    #                         final_status = "Failed"
    #                     elif color == "aborted":
    #                         final_color = " 🟣 "
    #                         final_status = "Aborted"
    #                     else:
    #                         final_color = " ⚫ "
    #                         final_status = "Unknown"

    #                     job_link = f"/job/{job_name}"
    #                     markdown_url = f"[{job_link}]({url})"
                        
    #                     table_rows.append({
    #                         "Name": name,
    #                         "Type": project_type,
    #                         "URL": markdown_url,
    #                         "Status": final_status,
    #                         "Color": final_color,
    #                     })
    #                 card = res.new_card()
    #                 card.theme = "modern-inline"
    #                 card.title = "# Jobs"
    #                 res.card = card
                    
    #                 slide = res.new_slide()
    #                 slide.type = "table"
    #                 slide.title = "*Job Details*"

    #                 headers = ["Name", "Type", "URL", "Status", "Color"]
                    
    #                 slide.data = {
    #                     "headers": headers,
    #                     "rows": table_rows
    #                 }
    #                 res.add_slides(slide)
    #             else:
    #                 text = "No jobs found on the Jenkins server."

    #         except Exception as e:
    #             text = f"Failed to fetch jobs. Error: {e}"

    res.text = text
    return res


@suggestion_handler
def suggester(req: CommandHandlerRequest, res: List[CommandSuggestion], *args):
    return res

def get_form():
    form = command.new_handler_response().new_form()
    form.title = 'Connect to Jenkins'
    form.hint = 'Connect to Jenkins Server'
    form.name = 'connect'
    form.button_label = 'Connect'
    form.version = 1

    actions = form.new_form_actions_obj()
    actions.submit = actions.new_form_action('formfn')

    form.actions = actions

    # host = form.new_form_input()
    # host.type = 'select'
    # host.name = 'host_type'
    # host.label = 'Host Type'
    # host.hint = 'Select the type of hosting'
    # host.placeholder = 'localhost'
    # host.mandatory = True
    # host.trigger_on_change = True

    # options = ['Localhost', 'Remote Server']
    # values = ['localhost', 'remote']

    # for option,value in zip(options, values):
    #     formvalue = host.new_form_value(option, value)
    #     host.add_options(formvalue)

    # form.add_inputs(host)

    url = form.new_form_input()
    url.type = 'text'
    url.name = 'url'
    url.label = 'URL'
    url.hint = 'Please enter your Jenkins Server URL'
    url.placeholder = 'http://localhost:8080/'
    url.mandatory = True
    url.value = ''
    form.add_inputs(url)

    user_name = form.new_form_input()
    user_name.type = 'text'
    user_name.name = 'username'
    user_name.label = 'Username'
    user_name.hint = 'Please enter your Username'
    user_name.placeholder = 'Zenkins'
    user_name.mandatory = True
    user_name.value = ''
    form.add_inputs(user_name)


    api_key = form.new_form_input()
    api_key.type = 'text'
    api_key.name = 'apiKey'
    api_key.label = 'API Key'
    api_key.hint = 'Enter your password or API Key'
    api_key.placeholder = "1102d6b43c7b403adbe44b9b14aeede192"
    api_key.mandatory = True
    
    form.add_inputs(api_key)
    return form

# def form2():
#     form = command.new_handler_response().new_form()
#     form.title = 'Create a Job'
#     form.hint = 'creates a new job in the Jenkins'
#     form.name = 'createjob'
#     form.button_label = 'Create'
#     form.version = 1

#     actions = form.new_form_actions_obj()
#     actions.submit = actions.new_form_action('createjob')

#     form.actions = actions

#     jobname = form.new_form_input()
#     jobname.type = 'text'
#     jobname.name = 'jobname'
#     jobname.label = 'Job Name'
#     jobname.hint = 'Please enter the Job Name'
#     jobname.placeholder = 'Zenkins'
#     jobname.mandatory = True
#     jobname.value = ''
#     form.add_inputs(jobname)

#     config = form.new_form_input()
#     config.type = 'textarea'
#     config.name = 'config'
#     config.label = 'XML Configuration file'
#     config.hint = 'Please enter your job config file'
#     config.placeholder = "<?xml version='1.1' encoding='UTF-8'?><project>...</project>"
#     config.mandatory = True
#     config.value = ''
#     form.add_inputs(config)


#     # api_key = form.new_form_input()
#     # api_key.type = 'text'
#     # api_key.name = 'apiKey'
#     # api_key.label = 'API Key'
#     # api_key.hint = 'Enter your password or API Key'
#     # api_key.placeholder = "1102d6b43c7b403adbe44b9b14aeede192"
#     # api_key.mandatory = True
    
#     # form.add_inputs(api_key)
#     return form

# def form4(job_names):
#     form = command.new_handler_response().new_form()
#     form.title = 'Delete Job/Jobs'
#     form.name = 'deletejob'
#     form.hint = 'Delete Jenkins Jobs'
#     form.button_label = 'Delete'

#     input1 = form.new_form_input()
#     input1.type = 'select'
#     input1.max_selections = 10
#     input1.multiple = True
#     input1.name = 'jobname'
#     input1.label = 'Job Name'
#     input1.placeholder = 'Zenkins'
#     input1.hint = 'Please select the Jobs'
#     input1.mandatory = True
#     for job_name in job_names:
#         formvalue = input1.new_form_value(job_name, job_name)
#         input1.add_options(formvalue)

#     form.add_inputs(input1)
#     form.action = form.new_form_action('deletejob')
#     return form


def get_form2(job_names):
    if not job_names:
        msg = command.new_handler_response().new_message()
        msg.text = f'No Available Jobs to get config'
        msg.type = 'banner'
        msg.status = 'success'
        return msg
    form = command.new_handler_response().new_form()
    form.title = 'Get Job Config'
    form.name = 'getjobconfig'
    form.hint = 'Get Jenkins Job Config'
    form.button_label = 'Get'

    input1 = form.new_form_input()
    input1.type = 'select'
    input1.name = 'jobname'
    input1.label = 'Job Name'
    input1.placeholder = 'Zenkins'
    input1.hint = 'Please select the Job'
    input1.mandatory = True

    sanitized_job_names = [job_name.replace(" ", "_") for job_name in job_names]

    for original_job_name, sanitized_job_name in zip(job_names, sanitized_job_names):        
        formvalue = input1.new_form_value(original_job_name, sanitized_job_name)
        input1.add_options(formvalue)
    form.add_inputs(input1)
    form.action = form.new_form_action('formfn')
    return form

def get_form3():
    form = command.new_handler_response().new_form()
    form.title = 'Node Configuration'
    form.hint = 'Gets the Node Configuration'
    form.name = 'getnodeconfig'
    form.button_label = 'Get'
    form.version = 1

    actions = form.new_form_actions_obj()
    actions.submit = actions.new_form_action('formfn')

    form.actions = actions

    url = form.new_form_input()
    url.type = 'text'
    url.name = 'name'
    url.label = 'Name'
    url.hint = 'Please enter the new node name'
    url.placeholder = 'linux_node'
    url.mandatory = True
    url.value = ''
    form.add_inputs(url)

    user_name = form.new_form_input()
    user_name.type = 'text'
    user_name.name = 'path'
    user_name.label = 'Root Directory'
    user_name.hint = 'Please enter the root directory path'
    user_name.placeholder = '/var/jenkins_home'
    user_name.mandatory = True
    user_name.value = ''
    form.add_inputs(user_name)


    api_key = form.new_form_input()
    api_key.type = 'number'
    api_key.name = 'executors'
    api_key.label = 'Number of Executors'
    api_key.hint = 'Enter the number of executors'
    api_key.placeholder = "2"
    api_key.mandatory = True
    
    form.add_inputs(api_key)
    return form
