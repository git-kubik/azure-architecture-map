# data.py

# This module defines the data structures for nodes and subnodes used in the Cytoscape
# graph within the Dash application. It categorizes various Azure services under
# primary nodes and their respective subnodes for visualization and interaction.

# =============================================================================
# Central Node Definition
# =============================================================================

central_node = {
    'id': 'Azure_Architectures',       # Unique identifier for the central node
    'label': 'Azure Architectures',    # Display label for the central node
    'description': 'Central node for Azure Architectures',  # Brief description
    'class': 'central-node'             # CSS class for styling
}

# =============================================================================
# Primary Nodes Definitions
# =============================================================================

primary_nodes = {
    'Compute': 'Compute services in Azure',                        # Primary category: Compute
    'Networking': 'Networking services in Azure',                  # Primary category: Networking
    'Storage': 'Storage services in Azure',                        # Primary category: Storage
    'Identity_Security': 'Identity and Security services in Azure', # Primary category: Identity and Security
    'Databases': 'Database services in Azure',                      # Primary category: Databases
    'Integration': 'Integration services in Azure',                  # Primary category: Integration
    'Monitoring_Governance': 'Monitoring and Governance services in Azure' # Primary category: Monitoring and Governance
}

# =============================================================================
# Subnodes Definitions
# =============================================================================

subnodes = {
    'Compute': {
        'Virtual_Machines': 'Virtual Machines (VMs) provide scalable computing resources in Azure.',
        'App_Services': 'App Services are used to build, host, and scale web applications.',
        'Kubernetes': 'Azure Kubernetes Service (AKS) provides container orchestration and management.',
        'Functions': 'Azure Functions are serverless compute services that allow you to run event-driven code.'
    },
    'Networking': {
        'VNets': 'Virtual Networks (VNets) allow you to build isolated network environments in Azure.',
        'Load_Balancers': 'Load Balancers distribute network traffic across multiple servers.',
        'DNS': 'Azure DNS allows you to host your DNS domains and manage records.',
        'NSGs': 'Network Security Groups (NSGs) control network traffic in and out of Azure resources.'
    },
    'Storage': {
        'Blob_Storage': 'Blob Storage is used for storing unstructured data like text or binary data.',
        'File_Storage': 'File Storage provides fully managed file shares in the cloud.',
        'Managed_Disks': 'Managed Disks are used to store data for VMs and other Azure resources.',
        'Data_Lake': 'Azure Data Lake is a scalable data storage and analytics service.'
    },
    'Identity_Security': {
        'Azure_AD': 'Azure Active Directory (AD) is a cloud-based identity and access management service.',
        'RBAC': 'Role-Based Access Control (RBAC) allows you to manage who has access to Azure resources.',
        'Key_Vault': 'Azure Key Vault helps safeguard cryptographic keys and secrets.',
        'Security_Center': 'Azure Security Center provides unified security management and threat protection.'
    },
    'Databases': {
        'SQL_Database': 'Azure SQL Database is a fully managed relational database service.',
        'Cosmos_DB': 'Cosmos DB is a globally distributed NoSQL database service.',
        'MySQL_PostgreSQL': 'Azure offers fully managed MySQL and PostgreSQL databases.',
        'SQL_Managed_Instances': 'SQL Managed Instances are fully-managed SQL Server instances in Azure.'
    },
    'Integration': {
        'Logic_Apps': 'Azure Logic Apps allow you to automate workflows and integrate applications.',
        'Service_Bus': 'Azure Service Bus is a messaging service for reliable communication between services.',
        'Event_Grid': 'Event Grid enables event-based architectures in Azure.',
        'API_Management': 'API Management allows you to create, manage, and secure APIs.'
    },
    'Monitoring_Governance': {
        'Azure_Monitor': 'Azure Monitor provides full-stack monitoring across your applications and resources.',
        'Policy': 'Azure Policy helps enforce organizational standards and compliance.',
        'Cost_Management': 'Cost Management helps you track and optimize your Azure spending.',
        'Blueprints': 'Azure Blueprints automate governance for resource management and compliance.'
    }
}
