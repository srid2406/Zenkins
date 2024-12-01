import datetime
from zcatalyst_cliq.widget_handler import (
    view_handler,
    WidgetExecutionHandlerRequest,
    WidgetResponse
)
import zcatalyst_sdk
from ujenkins import JenkinsClient
from datetime import datetime, timezone


@view_handler
def view_handler(req: WidgetExecutionHandlerRequest, res: WidgetResponse, *args):
    res.type = 'applet'

    systems_tab = res.new_widget_tab('systemsTab', "System Info")
    job_tab = res.new_widget_tab('jobsTab', 'Jobs')
    build_tab = res.new_widget_tab('buildsTab', 'Builds')
    node_tab = res.new_widget_tab('nodesTab', 'Nodes')
    help_tab = res.new_widget_tab('helpTab', 'Help')


    res.add_tab(systems_tab, job_tab, build_tab, node_tab, help_tab)
    res.active_tab = systems_tab.id

    if req.event == 'load' or req.event == 'tab_click' and req.target.id == 'systemsTab' or req.event == 'refresh' and req.target.id == 'systemsTab':
        app = zcatalyst_sdk.get_app("test")
        cache_service = app.cache()
        segment_service = cache_service.segment()
        url = segment_service.get_value(req.user.id+"url")
        username = segment_service.get_value(req.user.id+"username")
        apiKey = segment_service.get_value(req.user.id+"apikey")
        if not (url and username and apiKey) :
            section = res.new_widget_section()
            section.id = '2'
            section_txt = section.new_widget_element()
            section_txt.type = "text"
            section_txt.text = "No active Jenkins connection. Please use the `connect` command first."
            section.add_elements(section_txt)
            res.add_sections(section)
        else:
            try:
                client = JenkinsClient(url, username, apiKey)
                sysInfo = client.system.get_status()
                version = client.system.get_version()
                sysVersion = f"{version[0]}.{version[1]}.{version[2]}"                
                sysIsReady = client.system.is_ready()
                jobsCount = len(client.jobs.get())
                nodesCount = len(client.nodes.get())
                mode = sysInfo.get("mode")
                slave_agent_port = sysInfo.get('slaveAgentPort')
                useSecurity = sysInfo.get('useSecurity')
                useCrumbs = sysInfo.get('useCrumbs')

                title_section = res.new_widget_section()
                title_section.id = '2'

                divider = title_section.new_widget_element() # common divider
                divider.type = 'divider'

                title_text = title_section.new_widget_element()
                title_text.type = "title"
                title_text.text = "Systems Info"

                restart_btn = title_text.new_widget_button()
                restart_btn.type = "invoke.function"
                restart_btn.id = "restartSys"
                restart_btn.name = "widgetfn"
                restart_btn.label = "Restart"
                restart_btn.emotion = "neutral"

                title_text.add_widget_buttons(restart_btn)

                title_section.add_elements(title_text, divider)

                basic_section = res.new_widget_section()
                basic_section.id = '3'

                # basic_title = basic_section.new_widget_element()
                # basic_title.type = "title"
                # basic_title.text = "Basic Details:"

                status_text = basic_section.new_widget_element()
                status_text.type = "text"
                status_text.text = f"Status: {'🟢 Ready' if sysIsReady else '🔴 Not Ready'}"
                status_subtext = basic_section.new_widget_element()
                status_subtext.type = "subtext"
                status_subtext.text = "Indicates if Jenkins is ready for operations."

                version_text = basic_section.new_widget_element()
                version_text.type = "text"
                version_text.text = f"Version: {sysVersion}"
                version_subtext = basic_section.new_widget_element()
                version_subtext.type = "subtext"
                version_subtext.text = "The current Jenkins system version."

                mode_text = basic_section.new_widget_element()
                mode_text.type = "text"
                mode_text.text = f"Mode: {mode}"
                mode_subtext = basic_section.new_widget_element()
                mode_subtext.type = "subtext"
                mode_subtext.text = "The operating mode of Jenkins (e.g., NORMAL or MAINTENANCE)."

                jobs_text = basic_section.new_widget_element()
                jobs_text.type = "text"
                jobs_text.text = f"Number of Jobs: {jobsCount}"
                jobs_subtext = basic_section.new_widget_element()
                jobs_subtext.type = "subtext"
                jobs_subtext.text = "The total number of jobs configured in Jenkins."

                nodes_text = basic_section.new_widget_element()
                nodes_text.type = "text"
                nodes_text.text = f"Number of Nodes: {nodesCount}"
                nodes_subtext = basic_section.new_widget_element()
                nodes_subtext.type = "subtext"
                nodes_subtext.text = "The number of nodes connected to the Jenkins master."

                slave_port_text = basic_section.new_widget_element()
                slave_port_text.type = "text"
                slave_port_text.text = f"Slave Agent Port: {slave_agent_port}"
                slave_port_subtext = basic_section.new_widget_element()
                slave_port_subtext.type = "subtext"
                slave_port_subtext.text = "The port used by slave agents to connect to the master."

                use_security_text = basic_section.new_widget_element()
                use_security_text.type = "text"
                use_security_text.text = f"Use Security: {useSecurity}"
                use_security_subtext = basic_section.new_widget_element()
                use_security_subtext.type = "subtext"
                use_security_subtext.text = "Indicates if security is enabled in Jenkins."

                # Use Crumbs
                use_crumbs_text = basic_section.new_widget_element()
                use_crumbs_text.type = "text"
                use_crumbs_text.text = f"Use Crumbs: {useCrumbs}"
                use_crumbs_subtext = basic_section.new_widget_element()
                use_crumbs_subtext.type = "subtext"
                use_crumbs_subtext.text = "Indicates if CSRF protection (crumbs) is enabled in Jenkins."

                basic_section.add_elements(
                    status_text, status_subtext, version_text, version_subtext,
                    mode_text, mode_subtext, jobs_text, jobs_subtext, nodes_text, nodes_subtext,
                    slave_port_text, slave_port_subtext, use_security_text, use_security_subtext,
                    use_crumbs_text, use_crumbs_subtext
                )
                        
                res.add_sections(title_section, basic_section)
            except Exception as e:
                    section = res.new_widget_section()
                    section.id = '2'
                    section_txt = section.new_widget_element()
                    section_txt.type = "text"
                    section_txt.text = f"Error: {e}"
                    section.add_elements(section_txt)
                    res.add_sections(section)
        return res

    elif req.event == 'tab_click' or req.event == 'refresh':
        target = req.target.id

        res.active_tab = target
        if target == 'buildsTab':
            app = zcatalyst_sdk.get_app("test")
            cache_service = app.cache()
            segment_service = cache_service.segment()
            url = segment_service.get_value(req.user.id+"url")
            username = segment_service.get_value(req.user.id+"username")
            apiKey = segment_service.get_value(req.user.id+"apikey")
            if not (url and username and apiKey) :
                section = res.new_widget_section()
                section.id = '2'
                section_txt = section.new_widget_element()
                section_txt.type = "text"
                section_txt.text = "No active Jenkins connection. Please use the `connect` command first."
                section.add_elements(section_txt)
                res.add_sections(section)
            else:
                try:
                    client = JenkinsClient(url, username, apiKey)
                    nodes = client.nodes.get()
                    nodeNames = list(nodes.keys())
                    builds = []
                    for node in nodeNames:
                        builds.extend(client.nodes.get_all_builds(node))

                    table_rows = []
                    for build in builds:
                        job_name = build['job_name']
                        build_number = build['number']
    
                        build_info = client.builds.get_info(job_name, build_number)
                        build_id = build_info.get('id') or 'N/A'
                        display_name = build_info.get('fullDisplayName') or 'N/A'
                        build_type = build_info.get('_class') or 'N/A'
                        started_by = next((cause.get('userName') for action in build_info['actions'] if 'causes' in action for cause in action['causes']), None) or 'N/A'
                        executor_utilization = next((action.get('executorUtilization') for action in build_info['actions'] if '_class' in action and action['_class'] == 'jenkins.metrics.impl.TimeInQueueAction'), None) or 'N/A'
                        artifacts = build_info.get('artifacts') or 'N/A'
                        result = build_info.get('result') or 'N/A'
                        duration = build_info.get('duration') or 'N/A'
                        url = build_info.get('url') or 'N/A'
                        timestamp = build_info.get('timestamp') or 'N/A'
                        is_building = build_info.get('building') or 'false'

                        if not timestamp == 'N/A': 
                            timestamp_seconds = timestamp / 1000
                            dt_object = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)

                            formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            formatted_time = 'N/A'

                        table_rows.append({
                                "ID": build_id,
                                "Type": build_type,
                                "Started By": started_by,
                                "Start time": formatted_time,
                                "Executor(s) utilized": executor_utilization,
                                "Artifacts": artifacts,
                                "Result": result,
                                "Duration": duration,
                                "Building": is_building,
                                "URL": url,
                            })

                    title_section = res.new_widget_section()
                    title_section.id = '2'

                    divider = title_section.new_widget_element() # common divider
                    divider.type = 'divider'

                    title_text = title_section.new_widget_element()
                    title_text.type = "title"
                    title_text.text = "Jenkins Builds"

                    start_btn = title_text.new_widget_button()
                    start_btn.type = "invoke.function"
                    start_btn.id = "startbuild"
                    start_btn.name = "widgetfn"
                    start_btn.label = "Start Build(s)"
                    start_btn.emotion = "positive"

                    # stop_btn = title_text.new_widget_button()
                    # stop_btn.type = "invoke.function"
                    # stop_btn.id = "stopbuild"
                    # stop_btn.name = "PyFnWidgetButton"
                    # stop_btn.label = "Stop Build(s)"
                    # stop_btn.emotion = "negative"

                    table = title_section.new_widget_element()
                    table.type = "table"
                    headers = ["ID", "Type", "Started By", "Start time", "Executor(s) utilized", "Artifacts", "Result", "Duration", "Building","URL"]
                    table.headers = headers
                    table.rows = table_rows

                    title_text.add_widget_buttons(start_btn)
                    title_section.add_elements(title_text, divider, table)
                    res.add_sections(title_section)
                except Exception as e:
                    section = res.new_widget_section()
                    section.id = '2'
                    section_txt = section.new_widget_element()
                    section_txt.type = "text"
                    section_txt.text = f"Error: {e}"
                    section.add_elements(section_txt)
                    res.add_sections(section)

        elif target == 'jobsTab':
            app = zcatalyst_sdk.get_app("test")
            cache_service = app.cache()
            segment_service = cache_service.segment()
            url = segment_service.get_value(req.user.id+"url")
            username = segment_service.get_value(req.user.id+"username")
            apiKey = segment_service.get_value(req.user.id+"apikey")
            if not (url and username and apiKey) :
                section = res.new_widget_section()
                section.id = '2'
                section_txt = section.new_widget_element()
                section_txt.type = "text"
                section_txt.text = "No active Jenkins connection. Please use the `connect` command first."
                section.add_elements(section_txt)
                res.add_sections(section)
            else:
                try:
                    client = JenkinsClient(url, username, apiKey)
                    jobs = client.jobs.get()
                    table_section = res.new_widget_section()
                    table_section.id = '3'

                    divider = table_section.new_widget_element() # common divider
                    divider.type = 'divider'

                    table_title = table_section.new_widget_element()
                    table_title.type = "title"
                    table_title.text = "Jenkins Jobs"

                    table = table_section.new_widget_element()
                    table.type = "table"
                    headers = ["Name", "Type", "URL", "Last Build", "Build Color"]
                    table.headers = headers

                    create_btn = table_title.new_widget_button()
                    create_btn.type = "invoke.function"
                    create_btn.id = "createjob"
                    create_btn.name = "widgetfn"
                    create_btn.label = "Create"
                    create_btn.emotion = "positive"

                    delete_btn = table_title.new_widget_button()
                    delete_btn.type = "invoke.function"
                    delete_btn.id = "deletejob"
                    delete_btn.name = "widgetfn"
                    delete_btn.label = "Delete"
                    delete_btn.emotion = "negative"

                    table_title.add_widget_buttons(create_btn, delete_btn)

                    if jobs:
                        table_rows = []  # Store rows for the table
                        for job_name, job_info in jobs.items():
                            
                            name = job_info.get('name', 'N/A')
                            url = job_info.get('url', 'N/A')
                            color = job_info.get('color', 'N/A')
                            project_type = job_info.get('_class', 'N/A')

                            if color == "blue":
                                final_color = " 🔵 "
                                final_status = "Success"
                            elif color == "notbuilt":
                                final_color = " ⚪ "
                                final_status = "Not Built"
                            elif color == "red":
                                final_color = " 🔴 "
                                final_status = "Failed"
                            elif color == "aborted":
                                final_color = " 🟣 "
                                final_status = "Aborted"
                            else:
                                final_color = " ⚫ "
                                final_status = "Unknown"

                            job_link = f"/job/{job_name}"
                            markdown_url = f"[{job_link}]({url})"
                            
                            table_rows.append({
                                "Name": name,
                                "Type": project_type,
                                "URL": markdown_url,
                                "Last Build": final_status,
                                "Build Color": final_color,
                            })
                    table.rows = table_rows
                    table_section.add_elements(table_title, divider, table)

                    res.add_sections(table_section)
                except Exception as e:
                    section = res.new_widget_section()
                    section.id = '2'
                    section_txt = section.new_widget_element()
                    section_txt.type = "text"
                    section_txt.text = f"Error: {e}"
                    section.add_elements(section_txt)
                    res.add_sections(section)

        elif target == "nodesTab":
            app = zcatalyst_sdk.get_app("test")
            cache_service = app.cache()
            segment_service = cache_service.segment()
            url = segment_service.get_value(req.user.id+"url")
            username = segment_service.get_value(req.user.id+"username")
            apiKey = segment_service.get_value(req.user.id+"apikey")
            if not (url and username and apiKey) :
                section = res.new_widget_section()
                section.id = '2'
                section_txt = section.new_widget_element()
                section_txt.type = "text"
                section_txt.text = "No active Jenkins connection. Please use the `connect` command first."
                section.add_elements(section_txt)
                res.add_sections(section)
            else:
                try:
                    client = JenkinsClient(url, username, apiKey)
                    nodes = client.nodes.get()
                    node_data = []

                    for node_name, node_info in nodes.items():
                        name = node_name
                        idle = node_info.get('idle', False)
                        jnlp_agent = node_info.get('jnlpAgent', False)
                        launch_supported = node_info.get('launchSupported', False)
                        num_executors = node_info.get('numExecutors', 0)
                        offline = node_info.get('offline', False)
                        _class = node_info.get('_class', '')

                        node_data.append({
                            "Node Name": name,
                            "Idle": idle,
                            "JNLP Agent": jnlp_agent,
                            "Launch Supported": launch_supported,
                            "Number of Executors": num_executors,
                            "Offline": offline,
                            "Class": _class
                        })
                    title_section = res.new_widget_section()
                    title_section.id = '2'

                    divider = title_section.new_widget_element() # common divider
                    divider.type = 'divider'

                    title_text = title_section.new_widget_element()
                    title_text.type = "title"
                    title_text.text = "Nodes"

                    table = title_section.new_widget_element()
                    table.type = "table"
                    headers = ["Node Name", "Idle", "JNLP Agent", "Launch Supported", "Number of Executors", "Offline", "Class"]
                    table.headers = headers
                    table.rows = node_data

                    create_btn = title_text.new_widget_button()
                    create_btn.type = "invoke.function"
                    create_btn.id = "createnode"
                    create_btn.name = "widgetfn"
                    create_btn.label = "Create"
                    create_btn.emotion = "positive"

                    delete_btn = title_text.new_widget_button()
                    delete_btn.type = "invoke.function"
                    delete_btn.id = "deletenode"
                    delete_btn.name = "widgetfn"
                    delete_btn.label = "Delete"
                    delete_btn.emotion = "negative"

                    title_text.add_widget_buttons(create_btn, delete_btn)

                    title_section.add_elements(title_text, divider, table)
                    res.add_sections(title_section)
                except Exception as e:
                    section = res.new_widget_section()
                    section.id = '2'
                    section_txt = section.new_widget_element()
                    section_txt.type = "text"
                    section_txt.text = f"Error: {e}"
                    section.add_elements(section_txt)
                    res.add_sections(section)
        elif target == "helpTab":
            title_section = res.new_widget_section()
            title_section.id = '2'

            divider = title_section.new_widget_element() # common divider
            divider.type = 'divider'

            title_text = title_section.new_widget_element()
            title_text.type = "title"
            title_text.text = "Help"

            title_section.add_elements(title_text, divider)

            commands_section  = res.new_widget_section()
            commands_section.id = '3'

            commands_title = commands_section.new_widget_element()
            commands_title.type = "title"
            commands_title.text = "Slash Commands"

            commands_text = commands_section.new_widget_element()
            commands_text.type = "text"
            commands_text.text = '1) `/connect`: Connects to the Jenkins Server.\n2) `/disconnect`: Disconnects the Jenkins Server. Use "/connect" to reconnect.\n3) `/getjobconfig`: Gets the Job configuration of an existing job.\n4) `/getnodeconfig`: Generates a Node configuration, which can be used in Node creation process.\n'

            divider = commands_section.new_widget_element() # common divider
            divider.type = 'divider'

            commands_section.add_elements(commands_title, commands_text, divider)

            widgets_section  = res.new_widget_section()
            widgets_section.id = '4'

            widgets_title = commands_section.new_widget_element()
            widgets_title.type = "title"
            widgets_title.text = "Widgets"

            widgets_text = commands_section.new_widget_element()
            widgets_text.type = "text"
            widgets_text.text = '1) `System Info Tab`: Displays the Jenkins Server information\n2) `Jobs Tab`: Displays the information about each Job. Also allows us to "Create" and "Delete" jobs.\n3) `Builds Tab`: Displays the information about each Build. Also allows us to "Start" builds.\n4) `Nodes Tab`: Displays the information about each Node. Also allows us to "Create" and "Delete" nodes.\n'

            divider = widgets_section.new_widget_element() # common divider
            divider.type = 'divider'

            widgets_section.add_elements(widgets_title, widgets_text, divider)

            contact_section  = res.new_widget_section()
            contact_section.id = '5'

            contact_title = contact_section.new_widget_element()
            contact_title.type = "title"
            contact_title.text = "Contact"

            contact_text = contact_section.new_widget_element()
            contact_text.type = "text"
            contact_text.text = '*More to come in future*. \n*Stay in Connect*\n`Zoho Mail`: sridamul@zohomail.com\n`GMail`: sridamul@gmail.com\n`Jenkins Author Page`: [Sridhar Sivakumar](https://www.jenkins.io/blog/authors/sridamul/)\n'

            divider = contact_section.new_widget_element() # common divider
            divider.type = 'divider'

            contact_section.add_elements(contact_title, contact_text, divider)

            res.add_sections(title_section, commands_section, widgets_section, contact_section)

            

    # first_nav = {
    #     'label': 'Page : 1',
    #     'type': 'invoke.function',
    #     'name': 'PyFnWidgetButton',
    #     'id': 'breadcrumbs'
    # }
   
    # link_button = {
    #     'label': 'Link',
    #     'type': 'open.url',
    #     'url': 'https://www.zoho.com'
    # }

    # banner_button = {
    #     'label': 'Banner',
    #     'type': 'invoke.function',
    #     'name': 'PyFnWidgetButton',
    #     'id': 'banner'
    # }

    # res.header = {
    #     'title' : 'Header 1',
    #     'navigation' : 'new',
    #     'buttons' : [first_nav, link_button, banner_button]
    # 

    # res.footer = {
    #     'text' : 'Footer text',
    #     'buttons' : [link_button, banner_button]
    # }
    return res
