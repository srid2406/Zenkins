from datetime import datetime
from zcatalyst_cliq import function_handler
from zcatalyst_cliq.function_handler import (
    button_function_handler,
    form_submit_handler,
    form_change_handler,
    form_dynamic_field_handler,
    widget_button_handler,
    ButtonFunctionRequest,
    FormFunctionRequest,
    WidgetFunctionRequest,
    HandlerResponse,
    FormChangeResponse,
    FormDynamicFieldResponse,
    WidgetResponse
)
from ujenkins import JenkinsClient, helpers
from ujenkins import exceptions
import zcatalyst_sdk
from time import sleep
import json
import logging
# import pyperclip

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()



@button_function_handler
def button_fn_handler(req: ButtonFunctionRequest, res: HandlerResponse, *args):
    # if req.name == "copy":
    #     app = zcatalyst_sdk.get_app("test")
    #     cache_service = app.cache()
    #     segment_service = cache_service.segment()
    #     url = segment_service.get_value(req.user.id+"url")
    #     username = segment_service.get_value(req.user.id+"username")
    #     apiKey = segment_service.get_value(req.user.id+"apikey")
    #     lastCopied = segment_service.get_value(req.user.id+"lastCopied")
    #     pyperclip.copy(lastCopied)
    #     msg = function_handler.new_handler_response().new_message()
    #     msg.text = f'Copied to Clipboard'
    #     msg.type = 'banner'
    #     msg.status = 'success'
    #     return msg
    # if req.name == "build":
        # app = zcatalyst_sdk.get_app("test")
        # cache_service = app.cache()
        # segment_service = cache_service.segment()
        # url = segment_service.get_value(req.user.id+"url")
        # username = segment_service.get_value(req.user.id+"username")
        # apiKey = segment_service.get_value(req.user.id+"apikey")
        # job_name = segment_service.get_value(req.user.id+"lastJob")
    #     if not (url and username and apiKey) :
    #         text = "No active Jenkins connection. Please use the `connect` command first."
    #         res.set_text(text)
    #     else:
    #         try:
    #             client = JenkinsClient(url, username, apiKey)
    #             result = client.builds.start(job_name)

    #             text = f"Build Triggered Successfully. 🚀"

    #             card = res.new_card()
    #             card.theme = "modern-inline"
    #             card.title = "Info"
    #             res.card = card
    #             res.set_text(text)

    #             slide = res.new_slide()
    #             slide.title = ''
    #             slide.type = "label"
    #             data_list = [
    #                 {"Job Name": job_name},
    #                 {"Build Queue ID": result},
    #             ]
    #             slide.data = data_list
    #             res.add_slides(slide)
    #         except Exception as e:
    #             card = res.new_card()
    #             card.title = "# Failed to trigger the job build."
    #             res.card = card
    #             res.set_text(f"```Failed: {e}```")
    #     return res
    # else:
    #     res.set_text(f"No function named {req.name}")
        return res


@form_submit_handler
def form_submit(req: FormFunctionRequest, res: HandlerResponse, *args):
    if req.form.name == "connect":
        try:
            values = req.form.values
            
            client = connect(values.url, values.username, values.apiKey)
            version = client.system.get_version()
            parsed_version = f"{version[0]}.{version[1]}.{version[2]}"
            status = client.system.get_status()
            slave_agent_port = status.get('slaveAgentPort')
            use_security = status.get('useSecurity')
            use_crumbs = status.get('useCrumbs')
            mode = status.get("mode")

            app = zcatalyst_sdk.get_app("test")
            cache_service = app.cache()
            segment_service = cache_service.segment()
            segment_service.put(req.user.id+'url', values.url)
            segment_service.put(req.user.id+'username', values.username)
            segment_service.put(req.user.id+'apikey', values.apiKey)

            segments = cache_service.get_all_segment()

            text = f"Hi *{req.user.first_name}*, \nThe connection to Jenkins was successful. :wink:"
            res.set_text(text)

            card = res.new_card()
            card.theme = "modern-inline"
            card.title = "# Connection Successful"
            res.card = card

            slide = res.new_slide()
            slide.type = "label"
            slide.title = "*Connection Details*"
            
            data_list = [
                {"Mode": mode},
                {"Version": parsed_version},
                {"Slave Agent Port": slave_agent_port},
                {"Use Security": use_security},
                {"URL": values.url},
            ]

            slide.data = data_list
            res.add_slides(slide)

        # except exceptions.JenkinsNotFoundError as e:
        #     card = res.new_card()
        #     card.title = "Connection Failed"
        #     res.card = card
        #     res.set_text(f"404 :sad: Page Not Found")

        except Exception as e:
            card = res.new_card()
            card.title = "# Connection Failed"
            res.card = card
            if "401 Unauthorized" in str(e):
                res.set_text(f"Authentication error. Please check your username or API key. \n\n```Error: {e}```")
            else:
                res.set_text(f"```Connection Failed: {e}```")

        return res
    # elif req.form.name == "getconfig":
    #     app = zcatalyst_sdk.get_app("test")
    #     cache_service = app.cache()
    #     segment_service = cache_service.segment()
    #     url = segment_service.get_value(req.user.id+"url")
    #     username = segment_service.get_value(req.user.id+"username")
    #     apiKey = segment_service.get_value(req.user.id+"apikey")
    #     if not (url and username and apiKey) :
    #         text = "No active Jenkins connection. Please use the `connect` command first."
    #         res.set_text(text)
    #     else:
    #         try:
    #             values = req.form.values
    #             client = JenkinsClient(url, username, apiKey)
    #             config = client.jobs.get_config(values.jobname)
    #             txt = f"Here is the Config: {config}"

    #             res.set_text(txt)
    #             card = res.new_card()
    #             card.title = "Info"
    #             res.card = card
    #             return res
    #         except Exception as e:
    #             msg = function_handler.new_handler_response().new_message()
    #             msg.text = f'Try Again {e}'
    #             msg.type = 'banner'
    #             msg.status = 'failure'
    #             return msg
    # elif req.form.name == "createjob":
    #     app = zcatalyst_sdk.get_app("test")
    #     cache_service = app.cache()
    #     segment_service = cache_service.segment()
    #     url = segment_service.get_value(req.user.id+"url")
    #     username = segment_service.get_value(req.user.id+"username")
    #     apiKey = segment_service.get_value(req.user.id+"apikey")
    #     if not (url and username and apiKey) :
    #         text = "No active Jenkins connection. Please use the `connect` command first."
    #         res.set_text(text)
    #     else:
    #         try:
    #             values = req.form.values
    #             client = JenkinsClient(url, username, apiKey)
    #             if client.jobs.is_exists(values.jobname):
    #                 text = f"*Ooh Oh! Job with name '{values.jobname}' already exists.*"
    #                 res.set_text(text)
    #                 card = res.new_card()
    #                 card.title = "Info"
    #                 res.card = card
    #                 return res
    #             result = client.jobs.create(values.jobname, values.config)
    #             job_info = client.jobs.get_info(values.jobname)
    #             job_name = job_info.get("name")
    #             job_url = job_info.get("url")
    #             job_buildable = job_info.get("buildable")
    #             job_type = job_info.get("_class")
    #             job_description = job_info.get("description") or 'N/A'
    #             job_health = job_info.get("healthReport")

    #             # Add the Last Job name to cache to trigger the build
    #             segment_service.put(req.user.id+"lastJob", job_name)

    #             # text = f"{job_type}, {job_health}"
    #             text = f"Hurray! The Job `{values.jobname}` has been created successfully. :wink:"
    #             res.set_text(text)

    #             card = res.new_card()
    #             card.title = "*Job Creation Successful*"
    #             res.card = card
    #             slideList = []
    #             slide0 = res.new_slide()
    #             slide0.title = "Basic Details"
    #             slide0.type = "label"

    #             data_list = [
    #                 {'Job name': job_name},
    #                 {'Type': job_type},
    #                 {'Description': job_description},
    #                 {'Job Buildable': job_buildable},
    #                 {'Job URL': job_url},
    #             ]


    #             slide0.data = data_list
    #             slideList.append(slide0)

    #             # slide1 = res.new_slide()
    #             # slide1.title = "Health Report"
    #             # slide1.type = "label"
                
    #             # data_list1 = [
    #             #     {'Health Report Description': job_health[0]},
    #             #     {'Health Score': job_health[0]['score']}
    #             # ]
                
    #             # slide1.data = data_list1
    #             # slideList.append(slide1)
    #             button = slide0.new_button_obj()
    #             button.label = 'Start Build'
    #             button.key = "startbuild"
    #             button.type = '+'
    #             button.hint = 'Click to trigger the build process'

    #             action = button.new_action_object()
    #             action.type = 'invoke.function'

    #             action_data = action.new_action_data_obj()
    #             action_data.name = "build"
    #             action_data.owner = "sridamul@gmail.com"
                        
    #             action.data = action_data
    #             button.action= action
    #             slide0.add_buttons(button)

    #             res.slides = slideList
    #             # sleep(5)
    #         except Exception as e:
    #             card = res.new_card()
    #             card.title = "# Job Creation Failed"
    #             res.card = card
    #             res.set_text(f"```Creation Failed: {e}```")

    #     return res
    elif req.form.name == "createNode":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Please connect to Jenkins Server'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
        else:
            try:
                values = req.form.values
                client = JenkinsClient(url, username, apiKey)
                if client.nodes.is_exists(values.nodename):
                    LOGGER.log(logging.INFO, "Node already Exists")
                    msg = function_handler.new_handler_response().new_message()
                    msg.text = f"*Ooh Oh! Node with name '{values.nodename}' already exists.*"
                    msg.type = 'banner'
                    msg.status = 'failure'
                    return msg
                config_str = values.config.replace("'", "\"")
                try:
                    config_dict = json.loads(config_str)
                    result = client.nodes.create(values.nodename, config_dict)
                    LOGGER.log(logging.INFO, "Node Created")
                    msg = function_handler.new_handler_response().new_message()
                    msg.text = 'Node Created Successfully'
                    msg.type = 'banner'
                    msg.status = 'success'
                    return msg
                except json.JSONDecodeError as e:
                    LOGGER.log(logging.ERROR, f"{e}")
                    msg = function_handler.new_handler_response().new_message()
                    msg.text = f'Failed to parse config'
                    msg.type = 'banner'
                    msg.status = 'failure'
                    return msg

            except Exception as e:
                LOGGER.log(logging.ERROR, f"{e}")
                msg = function_handler.new_handler_response().new_message()
                msg.text = f'Failed to parse config: {e}'
                msg.type = 'banner'
                msg.status = 'failure'
                return msg
    elif req.form.name == "deletenode":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Please connect to Jenkins Server'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
        else:
            try:
                values = req.form.values
                client = JenkinsClient(url, username, apiKey)
                selected_values = []
                for node in values.nodename:
                    selected_values.append(node.label)
                for value in selected_values:
                    client.nodes.delete(value)
                msg = function_handler.new_handler_response().new_message()
                msg.text = 'Node Deleted Successfully'
                msg.type = 'banner'
                msg.status = 'success'
                return msg
            except Exception as e:
                msg = function_handler.new_handler_response().new_message()
                msg.text = 'Failed to Delete the Node'
                msg.type = 'banner'
                msg.status = 'failure'
                return msg
    elif req.form.name == "createjob":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Please connect to Jenkins Server'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
        else:
            try:
                values = req.form.values
                client = JenkinsClient(url, username, apiKey)
                if client.jobs.is_exists(values.jobname):
                    msg = function_handler.new_handler_response().new_message()
                    msg.text = f"*Ooh Oh! Job with name '{values.jobname}' already exists.*"
                    msg.type = 'banner'
                    msg.status = 'failure'
                    return msg
                result = client.jobs.create(values.jobname, values.config)
                msg = function_handler.new_handler_response().new_message()
                LOGGER.log(logging.INFO, "Job Created")
                msg.text = 'Job Created Successfully'
                msg.type = 'banner'
                msg.status = 'success'
                return msg
            except Exception as e:
                msg = function_handler.new_handler_response().new_message()
                msg.text = 'Job Creation Failed'
                msg.type = 'banner'
                msg.status = 'failure'
                return msg
    elif req.form.name == "deletejob":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            # text = "No active Jenkins connection. Please use the `connect` command first."
            # res.set_text(text)
            # return res
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Please connect to Jenkins Server'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
        try:
            values = req.form.values
            client = JenkinsClient(url, username, apiKey)
            selected_values = []
            for job in values.jobname:
                selected_values.append(job.label)
            for value in selected_values:
                client.jobs.delete(value)
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Jobs Deleted Successfully'
            msg.type = 'banner'
            msg.status = 'success'
            return msg
        except Exception as e:
            msg = function_handler.new_handler_response().new_message()
            msg.text = f'Job Deletion Failed'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
    elif req.form.name == "startbuild":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            # text = "No active Jenkins connection. Please use the `connect` command first."
            # res.set_text(text)
            # return res
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Please connect to Jenkins Server'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
        try:
            values = req.form.values
            client = JenkinsClient(url, username, apiKey)
            selected_values = []
            for job in values.jobname:
                selected_values.append(job.label)
            for value in selected_values:
                client.builds.start(value)
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Build(s) started Successfully'
            msg.type = 'banner'
            msg.status = 'success'
            return msg
        except Exception as e:
            msg = function_handler.new_handler_response().new_message()
            msg.text = f'Failed to Start build {e}'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
    elif req.form.name == "getjobconfig":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Please connect to Jenkins Server'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
        else:
            try:
                values = req.form.values
                client = JenkinsClient(url, username, apiKey)
                config = client.jobs.get_config(values.jobname.label)
                card = res.new_card()
                card.title = f"Job Config: `{values.jobname.label}`"
                res.card = card
                res.set_text(f"```{config}```")
                # segment_service.put(req.user.id+"lastCopied", config)
                # button = res.new_button()
                # button.label = 'Copy'
                # button.key = "copy"
                # button.type = '+'
                # button.hint = 'Copy to Clipboard'

                # action = button.new_action_object()
                # action.type = 'invoke.function'

                # action_data = action.new_action_data_obj()
                # action_data.name = "copy"
                # action_data.owner = "sridamul@gmail.com"
                        
                # action.data = action_data
                # button.action= action
                # res.add_button(button)
                return res
                # msg = function_handler.new_handler_response().new_message()
                # msg.text = 'Node Deleted Successfully'
                # msg.type = 'banner'
                # msg.status = 'success'
                # return msg
            except Exception as e:
                msg = function_handler.new_handler_response().new_message()
                msg.text = 'Failed to get the Job Config'
                msg.type = 'banner'
                msg.status = 'failure'
                return msg
    elif req.form.name == "getnodeconfig":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Please connect to Jenkins Server'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
        else:
            try:
                values = req.form.values
                client = JenkinsClient(url, username, apiKey)
                name = values.name
                path = values.path
                executors = values.executors
                config = helpers.construct_node_config(name=name, remote_fs=path, executors=executors)
                card = res.new_card()
                card.title = f"Node Config: `{name}`"
                res.card = card
                res.set_text(f"```{config}```")
                return res
            except Exception as e:
                msg = function_handler.new_handler_response().new_message()
                msg.text = 'Failed to get the Node Configuration.\nPlease check you details.'
                msg.type = 'banner'
                msg.status = 'failure'
                return msg

    else:
        res.set_text(f"No function named {req.form.name}")
        return res


@form_change_handler
def change_form(req: FormFunctionRequest, res: FormChangeResponse, *args):
    # target = req.target.name
    # values = req.form.values
    # field_value = values.host_type.value
    # if target == "host_type":
    #     if field_value == "localhost":
    #         select_box_action = res.new_form_modification_action()
    #         select_box_action.type = 'add_after'
    #         select_box_action.name = 'host_type'

    #         port = select_box_action.new_form_input()
    #         port.type = 'text'
    #         port.name = 'port'
    #         port.label = 'Port'
    #         port.hint = 'Enter the port of Jenkins host'
    #         port.placeholder = '8080'
    #         port.mandatory = True

    #         select_box_action.input = port

    #         remove_mobile_OSAction = res.new_form_modification_action()
    #         remove_mobile_OSAction.type = 'remove'
    #         remove_mobile_OSAction.name = 'url'

    #         res.add_actions(select_box_action, remove_mobile_OSAction)
    #     elif field_value == "remote":
    #         select_box_action = res.new_form_modification_action()
    #         select_box_action.type = 'add_after'
    #         select_box_action.name = 'host_type'

    #         url = select_box_action.new_form_input()
    #         url.type = 'text'
    #         url.name = 'url'
    #         url.label = 'URL'
    #         url.hint = 'Please enter your Jenkins Server URL'
    #         url.placeholder = 'https://DOMAIN:8080/'
    #         url.mandatory = True
    #         url.value = ''

    #         select_box_action.input = url

    #         remove_mobile_OSAction = res.new_form_modification_action()
    #         remove_mobile_OSAction.type = 'remove'
    #         remove_mobile_OSAction.name = 'port'

    #         res.add_actions(select_box_action, remove_mobile_OSAction)

    return res


@form_dynamic_field_handler
def handle_dynamic_field(req: FormFunctionRequest, res: FormDynamicFieldResponse, *args):
    return res


@widget_button_handler
def widget_button(req: WidgetFunctionRequest, res: WidgetResponse, *args):
    id = req.target.id

    if id == "createjob":
        return form2()
    elif id =="createnode":
        return form6()
    elif id == "deletenode":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")

        client = JenkinsClient(url, username, apiKey)
        nodes = client.nodes.get()
        nodeNames = list(nodes.keys())
        # display_names = [node_info['displayName'] for node_info in nodes.values()]

        return form7(nodeNames)
        # return form4(display_names)
    elif id == "startbuild":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")

        client = JenkinsClient(url, username, apiKey)
        jobs = client.jobs.get()
        job_names = [job_info['name'] for job_info in jobs.values()]
        return form4(job_names)
    elif id == "deletejob":
        try:
            app = zcatalyst_sdk.get_app("test")
            cache_service = app.cache()
            segment_service = cache_service.segment()
            url = segment_service.get_value(req.user.id+"url")
            username = segment_service.get_value(req.user.id+"username")
            apiKey = segment_service.get_value(req.user.id+"apikey")

            client = JenkinsClient(url, username, apiKey)
            jobs = client.jobs.get()
            job_names = [job_info['name'] for job_info in jobs.values()]
            return form3(job_names)
        except Exception as e:
            msg = function_handler.new_handler_response().new_message()
            msg.text = f'Deletion Failed. Try again. {e}'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
    elif id == "restartSys":
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        try:
            client = JenkinsClient(url, username, apiKey)
            # client.system.restart()
            sleep(10)
            msg = function_handler.new_handler_response().new_message()
            msg.text = 'Restarted Jenkins Successfully'
            msg.type = 'banner'
            msg.status = 'success'
            return msg
        except Exception as e:
            msg = function_handler.new_handler_response().new_message()
            msg.text = f'Restart Failed. Try again. {e}'
            msg.type = 'banner'
            msg.status = 'failure'
            return msg
def connect(jenkins_url, username, api_key):
    client = JenkinsClient(jenkins_url, username, api_key)
    return client


def form2():
    form = function_handler.new_handler_response().new_form()
    form.title = 'Create a Job'
    form.name = 'createjob'
    form.hint = 'Creates a new job in the Jenkins'
    form.button_label = 'Create'

    input1 = form.new_form_input()
    input1.type = 'text'
    input1.name = 'jobname'
    input1.label = 'Job Name'
    input1.placeholder = 'Zenkins'
    input1.hint = 'Please enter your Job name'
    input1.mandatory = True

    input2 = form.new_form_input()
    input2.type = 'textarea'
    input2.name = 'config'
    input2.label = 'XML Configuration file'
    input2.value = ''
    input2.mandatory = True
    input2.hint = 'Please enter your job config file'
    input2.placeholder = "<?xml version='1.1' encoding='UTF-8'?><project>...</project>"


    form.add_inputs(input1, input2)
    form.action = form.new_form_action('formfn')
    return form

def form3(job_names):
    if not job_names:
        LOGGER.log(logging.INFO, f"Empty Jobs")
        msg = function_handler.new_handler_response().new_message()
        msg.text = f'No Available Jobs to delete'
        msg.type = 'banner'
        msg.status = 'success'
        return msg
    LOGGER.log(logging.INFO, f"Form Creation Started")

    form = function_handler.new_handler_response().new_form()
    form.title = 'Delete Job(s)'
    form.name = 'deletejob'
    form.hint = 'Delete Jenkins Jobs'
    form.button_label = 'Delete'
    LOGGER.log(logging.INFO, f"Adding input")

    input1 = form.new_form_input()
    input1.type = 'select'
    input1.max_selections = 10
    input1.multiple = True
    input1.name = 'jobname'
    input1.label = 'Job Name'
    input1.placeholder = 'Zenkins'
    input1.hint = 'Please select the Jobs'
    input1.mandatory = True
    sanitized_job_names = [job_name.replace(" ", "_") for job_name in job_names]

    for original_job_name, sanitized_job_name in zip(job_names, sanitized_job_names):
        LOGGER.log(logging.INFO, f"Adding Job: {sanitized_job_name}")
        
        formvalue = input1.new_form_value(original_job_name, sanitized_job_name)
        input1.add_options(formvalue)

    form.add_inputs(input1)
    form.action = form.new_form_action('formfn')
    LOGGER.log(logging.INFO, f"{form}")
    return form

def form4(job_names):
    if not job_names:
        msg = function_handler.new_handler_response().new_message()
        msg.text = f'No Available Jobs to start build. Please create one.'
        msg.type = 'banner'
        msg.status = 'failure'
        return msg
    form = function_handler.new_handler_response().new_form()
    form.title = 'Start Build(s)'
    form.name = 'startbuild'
    form.hint = 'Start Jenkins Job build'
    form.button_label = 'Start'

    input1 = form.new_form_input()
    input1.type = 'select'
    input1.max_selections = 10
    input1.multiple = True
    input1.name = 'jobname'
    input1.label = 'Job Name'
    input1.placeholder = 'Zenkins'
    input1.hint = 'Please select the Job(s)'
    input1.mandatory = True
    sanitized_job_names = [job_name.replace(" ", "_") for job_name in job_names]

    for original_job_name, sanitized_job_name in zip(job_names, sanitized_job_names):
        LOGGER.log(logging.INFO, f"Adding Job: {sanitized_job_name}")
        
        formvalue = input1.new_form_value(original_job_name, sanitized_job_name)
        input1.add_options(formvalue)

    form.add_inputs(input1)
    form.action = form.new_form_action('formfn')
    return form

def form6():
    form = function_handler.new_handler_response().new_form()
    form.title = 'Create a Node'
    form.name = 'createNode'
    form.hint = 'Creates a new Node in the Jenkins'
    form.button_label = 'Create'

    input1 = form.new_form_input()
    input1.type = 'text'
    input1.name = 'nodename'
    input1.label = 'Node Name'
    input1.placeholder = 'Zenkins'
    input1.hint = 'Please enter your Node name'
    input1.mandatory = True

    input2 = form.new_form_input()
    input2.type = 'textarea'
    input2.name = 'config'
    input2.label = 'Node Configuration file'
    input2.value = ''
    input2.mandatory = True
    input2.hint = 'Please enter your Node configuration'
    input2.placeholder = "Tip: If you're not sure about the Node config, use /getnodeconfig to get the Configuration."


    form.add_inputs(input1, input2)
    form.action = form.new_form_action('formfn')
    return form

def form7(nodeNames):
    if not nodeNames:
        msg = function_handler.new_handler_response().new_message()
        msg.text = f'Please try again.'
        msg.type = 'banner'
        msg.status = 'failure'
        return msg
    form = function_handler.new_handler_response().new_form()
    form.title = 'Delete Node(s)'
    form.name = 'deletenode'
    form.hint = 'Delete Jenkins Node(s)'
    form.button_label = 'Delete'

    input1 = form.new_form_input()
    input1.type = 'select'
    input1.max_selections = 2
    input1.multiple = True
    input1.name = 'nodename'
    input1.label = 'Node Name'
    input1.placeholder = 'Zenkins'
    input1.hint = 'Please select the Node(s)'
    input1.mandatory = True
    nodeNames.remove("Built-In Node")

    sanitized_job_names = [job_name.replace(" ", "_") for job_name in nodeNames]

    for original_job_name, sanitized_job_name in zip(nodeNames, sanitized_job_names):
        LOGGER.log(logging.INFO, f"Adding Job: {sanitized_job_name}")
        
        formvalue = input1.new_form_value(original_job_name, sanitized_job_name)
        input1.add_options(formvalue)

    form.add_inputs(input1)
    form.action = form.new_form_action('formfn')
    return form

# def form5(running_builds):
#     if not running_builds:
#         msg = function_handler.new_handler_response().new_message()
#         msg.text = f'No Running Builds.'
#         msg.type = 'banner'
#         msg.status = 'success'
#         return msg
#     form = function_handler.new_handler_response().new_form()
#     form.title = 'Stop Build(s)'
#     form.name = 'stopbuild'
#     form.hint = 'Stop a running build'
#     form.button_label = 'Stop'

#     input1 = form.new_form_input()
#     input1.type = 'select'
#     input1.max_selections = 10
#     input1.multiple = True
#     input1.name = 'buildname'
#     input1.label = 'Build Names'
#     input1.placeholder = 'Zenkins'
#     input1.hint = 'Please select the build(s)'
#     input1.mandatory = True

#     for build in running_builds.keys():
#         formvalue = input1.new_form_value(build, build)
#         input1.add_options(formvalue)

#     form.add_inputs(input1)
#     form.action = form.new_form_action('createjobwidget')
#     return form