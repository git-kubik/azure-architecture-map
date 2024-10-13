# DATA.md

## Overview of `data.py`

The `data.py` file is a foundational component of the Azure Architecture Map application. It contains the data definitions for the central node, primary nodes, and subnodes that represent Azure services and their relationships. This data is used to construct the elements of the graph displayed in the application, providing the content and structure necessary for visualization.

---

## Table of Contents

- [Purpose of `data.py`](#purpose-of-datapy)
- [Data Structures](#data-structures)
  - [1. Central Node](#1-central-node)
  - [2. Primary Nodes](#2-primary-nodes)
  - [3. Subnodes](#3-subnodes)
- [Detailed Explanation](#detailed-explanation)
  - [Central Node Definition](#central-node-definition)
  - [Primary Nodes Definition](#primary-nodes-definition)
  - [Subnodes Definition](#subnodes-definition)
- [How `data.py` Fits into the Application](#how-datapy-fits-into-the-application)
- [Customization](#customization)
  - [Adding New Nodes](#adding-new-nodes)
  - [Modifying Existing Nodes](#modifying-existing-nodes)
  - [Data Consistency](#data-consistency)
- [Conclusion](#conclusion)

---

## Purpose of `data.py`

- **Data Source**: Provides the core data representing Azure services and their hierarchical relationships.
- **Graph Construction**: Supplies the necessary information to build the graph elements (nodes and edges) for visualization.
- **Separation of Concerns**: Isolates data definitions from application logic, making it easier to manage and update the content.

---

## Data Structures

The `data.py` file defines three primary data structures:

1. **Central Node**: Represents the root or central concept in the graph (e.g., "Azure").
2. **Primary Nodes**: Direct children of the central node, representing major categories of Azure services.
3. **Subnodes**: Children of primary nodes, representing specific services within each category.

### 1. Central Node

```python
central_node = {
    'id': 'Azure',
    'label': 'Azure',
    'description': 'Microsoft Azure is a cloud computing service created by Microsoft for building, testing, deploying, and managing applications and services.'
}
```

- **id**: Unique identifier for the central node.
- **label**: Display name for the node in the graph.
- **description**: A brief description of the node's purpose.

### 2. Primary Nodes

```python
primary_nodes = {
    'Compute': 'Services related to computing power and hosting applications.',
    'Storage': 'Services related to data storage solutions.',
    'Networking': 'Services related to networking and content delivery.',
    'Databases': 'Services related to database management systems.',
    'Security': 'Services that provide security, identity, and access management.',
    # Additional primary nodes can be added here.
}
```

- **Keys**: Unique identifiers for primary nodes (e.g., 'Compute', 'Storage').
- **Values**: Descriptions of each primary node category.

### 3. Subnodes

```python
subnodes = {
    'Compute': {
        'Virtual Machines': 'Provision Windows and Linux virtual machines in seconds.',
        'App Services': 'Quickly create powerful cloud apps for web and mobile.',
        'Container Instances': 'Easily run containers on Azure without managing servers.',
        # Additional compute subnodes can be added here.
    },
    'Storage': {
        'Blob Storage': 'Massively scalable object storage for unstructured data.',
        'File Storage': 'Simple, secure and serverless enterprise-grade cloud file shares.',
        'Queue Storage': 'Effectively scale apps according to traffic fluctuations.',
        # Additional storage subnodes can be added here.
    },
    'Networking': {
        'Virtual Network': 'Provision private networks, optionally connect to on-premises datacenters.',
        'Load Balancer': 'Deliver high availability and network performance to your applications.',
        'CDN': 'Ensure secure, reliable content delivery with global reach.',
        # Additional networking subnodes can be added here.
    },
    'Databases': {
        'SQL Database': 'Managed, intelligent SQL in the cloud.',
        'Cosmos DB': 'Globally distributed, multi-model database service.',
        'Azure Database for PostgreSQL': 'Fully managed, intelligent, and scalable PostgreSQL.',
        # Additional database subnodes can be added here.
    },
    'Security': {
        'Security Center': 'Unified security management and advanced threat protection.',
        'Key Vault': 'Safeguard and maintain control of keys and other secrets.',
        'Azure Active Directory': 'Universal identity platform for all your apps.',
        # Additional security subnodes can be added here.
    },
    # Additional subnode categories can be added here.
}
```

- **Keys (First Level)**: Correspond to primary node identifiers.
- **Keys (Second Level)**: Unique identifiers for subnodes under each primary node.
- **Values**: Descriptions of each subnode service.

---

## Detailed Explanation

### Central Node Definition

The central node serves as the root of the graph, representing the overarching concept around which the rest of the nodes are organized.

- **ID and Label**: Both set to 'Azure' in this case, indicating that Azure is the central focus.
- **Description**: Provides a brief overview of Microsoft Azure, which can be displayed when the node is selected in the application.

### Primary Nodes Definition

Primary nodes represent major categories of Azure services. They are directly connected to the central node.

- **Categories**: Examples include 'Compute', 'Storage', 'Networking', 'Databases', and 'Security'.
- **Descriptions**: Offer a summary of what each category encompasses, aiding users in understanding the high-level organization of services.

### Subnodes Definition

Subnodes are specific services or features within each primary category. They are connected to their respective primary nodes.

- **Structure**: Each primary node key maps to a dictionary of subnodes.
- **Service Entries**:
  - **ID (Key)**: The name of the service (e.g., 'Virtual Machines', 'Blob Storage').
  - **Description (Value)**: A brief explanation of the service's functionality and benefits.
- **Flexibility**: Subnodes can be expanded by adding more services under each primary node.

---

## How `data.py` Fits into the Application

- **Data Provision**:
  - The data structures in `data.py` are imported by other modules (e.g., `layout.py`, `utils/helpers.py`) to construct the graph elements.
- **Graph Construction**:
  - Nodes and edges are created based on the relationships defined between the central node, primary nodes, and subnodes.
  - The data is transformed into a format compatible with the Cytoscape graph component.
- **User Interaction**:
  - Descriptions provided in the data are displayed when users interact with nodes, enhancing the informational value of the application.
- **Scalability**:
  - The modular structure allows for easy addition of new services and categories as Azure expands.

---

## Customization

### Adding New Nodes

To add new nodes to the graph:

1. **Add a New Primary Node**:

   - **Example**:

     ```python
     primary_nodes['AI and Machine Learning'] = 'Services for building and deploying AI solutions.'
     ```

   - **Add Corresponding Subnodes**:

     ```python
     subnodes['AI and Machine Learning'] = {
         'Cognitive Services': 'Add intelligent features to your applications.',
         'Machine Learning': 'Build and train machine learning models fast.'
     }
     ```

2. **Add a New Subnode to an Existing Primary Node**:

   - **Example**:

     ```python
     subnodes['Compute']['Batch'] = 'Cloud-scale job scheduling and compute management.'
     ```

### Modifying Existing Nodes

- **Change Descriptions**: Update the descriptions to provide more detailed information or reflect changes in services.
  - **Example**:

    ```python
    primary_nodes['Compute'] = 'Compute services including VMs, containers, and serverless functions.'
    ```

- **Rename Nodes**: Update the labels if services are rebranded or renamed.
  - **Ensure IDs remain unique** to prevent conflicts in the graph.

### Data Consistency

- **Unique Identifiers**: IDs used for nodes should be unique across all levels to prevent clashes.
- **Matching Keys**: When adding subnodes, ensure the primary node key exists in `primary_nodes`.
- **Descriptions**: Provide meaningful descriptions for each node to enhance user understanding.

---

## Conclusion

The `data.py` file is essential for defining the content and structure of the Azure Architecture Map application. By organizing Azure services into a hierarchical data structure, it allows for the construction of an interactive and informative graph that users can explore.

Understanding `data.py` enables developers and users to:

- **Customize the Graph**: Add, modify, or remove nodes to tailor the graph to specific needs or updates in Azure services.
- **Enhance User Experience**: Provide detailed descriptions and logical organization to help users navigate and understand Azure's offerings.
- **Maintain the Application**: Keep the application's data up-to-date with the latest Azure services and changes.

---

## Additional Notes

- **Data Source Updates**:
  - Regularly review and update `data.py` to reflect new services or changes announced by Microsoft Azure.
- **Automating Data Updates**:
  - Consider integrating with Azure's APIs or official documentation sources to automate data updates, ensuring the graph remains current.
- **Collaboration**:
  - When working in a team, establish guidelines for updating `data.py` to avoid conflicts and maintain consistency.

By effectively managing `data.py`, the Azure Architecture Map application remains a valuable tool for visualizing and understanding the complex ecosystem of Azure services.