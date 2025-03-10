# Zoho Cliq Extension for Jenkins

> [!NOTE]  
> WIP
> The Extension is not yet deployed to Zoho Marketplace

A **Jenkins Extension** for the **Zoho Cliq** platform, enabling users to manage Jenkins Jobs, Builds, and Nodes within Cliq using commands and widgets.

## Features

- **Zoho Catalyst Integration**: Utilized serverless functions for backend processing.
- **Jenkins API (ujenkins)**: Fetch and manage Jenkins Jobs, Builds, and Nodes.
- **Interactive Commands & Widgets**: View and trigger jobs directly from Zoho Cliq.
- **Helper Functions**: Generate Job and Build configurations dynamically.

## Technologies Used

- **Python**
- **Jenkins API (`ujenkins`)**
- **Zoho Catalyst**

## Handlers

- **Bot**: To make users comfortable with using the tool
- **Commands**: 
    - `/connect`: Connects to the Jenkins Server.
    - `/disconnect`: Disconnects the Jenkins Server. Use "/connect" to reconnect.
    - `/getjobconfig`: Gets the Job configuration of an existing job.
    - `/getnodeconfig`: Generates a Node configuration, which can be used in Node creation process.
- **Widgets**:
    - `System Info Tab`: Displays the Jenkins Server information
    - `Jobs Tab`: Displays the information about each Job. Also allows us to "Create" and "Delete" jobs.
    - `Builds Tab`: Displays the information about each Build. Also allows us to "Start" builds.
    - `Nodes Tab`: Displays the information about each Node. Also allows us to "Create" and "Delete" nodes.


## License

This project is licensed under the [MIT License](LICENSE).

## References:

Zoho Catalyst: https://catalyst.zoho.com/

Jenkins API: https://github.com/pbelskiy/ujenkins
