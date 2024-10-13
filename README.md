# Azure Architecture Map

A Dash application that visualizes Azure services in an interactive graph format. This tool helps users explore Azure's architectural components, understand relationships between services, and annotate nodes with custom notes for better comprehension and planning.

## Table of Contents

- [Azure Architecture Map](#azure-architecture-map)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Detailed Explanations](#detailed-explanations)
  - [Customization](#customization)
    - [Adding or Modifying Nodes](#adding-or-modifying-nodes)
    - [Changing Styles](#changing-styles)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **Interactive Graph Visualization**: Explore Azure services organized into categories and subcategories.
- **Node Interaction**: Click on nodes to view detailed information and add custom notes.
- **Search Functionality**: Search nodes using a case-insensitive substring search to quickly find services.
- **State Persistence**: Save and load the state of the graph, including node positions and custom notes.
- **Zoom Controls**: Easily zoom in, zoom out, and reset the zoom level for better navigation.
- **Responsive Layout**: The application layout adjusts to different screen sizes for optimal viewing.

## Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package installer)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/azure-architecture-map.git
   cd azure-architecture-map
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   cat > requirements.txt << *EOF*
   dash
   dash_cytoscape
   dash_bootstrap_components
   dash_extensions
   *EOF*
   ```

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application**

   ```bash
   python app.py
   ```

2. **Access the Application**

   Open your web browser and navigate to `http://127.0.0.1:8050/`.

3. **Explore the Graph**

   - **View Nodes**: Click on any node to see its details and description.
   - **Add Notes**: In the node information panel, add or edit notes and click "Save Note."
   - **Search Nodes**: Use the search bar to find nodes by typing any part of their labels.
   - **Zoom Controls**: Use the "Zoom In," "Zoom Out," and "Reset Zoom" buttons to navigate the graph.
   - **Save/Load State**: Click "Save State" to save the current graph state, including node positions and notes. Click "Load State" to restore the saved state.

## Project Structure

```
azure-architecture-map/
├── app.py
├── data.py
├── layout.py
├── callbacks.py
├── components/
│   └── graph.py
├── utils/
│   └── helpers.py
├── assets/
│   └── styles.css
├── logs/
│   └── app.log
├── graph_state.db
├── requirements.txt
├── README.md
└── docs/
    ├── APP.md
    ├── CALLBACKS.md
    ├── DATA.md
    ├── GRAPH.md
    ├── GRAPH_STATE.DB.md
    ├── HELPERS.md
    ├── LAYOUT.md
    └── STYLES.CSS.md
```

- **app.py**: Initializes the Dash application and sets up logging. See [APP.md](docs/APP.md) for a detailed explanation.
- **data.py**: Contains data definitions for the central node, primary nodes, and subnodes. See [DATA.md](docs/DATA.md) for more details.
- **layout.py**: Defines the layout of the application, including the graph and control panels. See [LAYOUT.md](docs/LAYOUT.md) for details.
- **callbacks.py**: Contains all the callback functions that handle user interactions. See [CALLBACKS.md](docs/CALLBACKS.md) for a detailed explanation.
- **components/graph.py**: Defines the Cytoscape graph component. See [GRAPH.md](docs/GRAPH.md) for more details.
- **utils/helpers.py**: Utility functions for graph construction, database interactions, and search functionality. See [HELPERS.md](docs/HELPERS.md) for more information.
- **assets/styles.css**: Custom CSS styles for the application. See [STYLES.CSS.md](docs/STYLES.CSS.md) for details.
- **logs/**: Directory where application logs are stored.
- **graph_state.db**: SQLite database file for persisting graph state. See [GRAPH_STATE.DB.md](docs/GRAPH_STATE.DB.md) for more information.
- **requirements.txt**: List of Python dependencies required by the application.
- **README.md**: The main readme file you are currently reading.
- **docs/**: Directory containing detailed documentation files.

## Detailed Explanations

For an in-depth understanding of each component of the application, please refer to the following documentation in the `docs/` directory:

- **[APP.md](docs/APP.md)**: Detailed explanation of `app.py`, including application initialization and configuration.
- **[CALLBACKS.md](docs/CALLBACKS.md)**: Comprehensive documentation of `callbacks.py`, explaining how user interactions are managed through callbacks.
- **[DATA.md](docs/DATA.md)**: Detailed explanation of `data.py`, describing the data structures used to represent Azure services.
- **[LAYOUT.md](docs/LAYOUT.md)**: In-depth explanation of `layout.py`, covering how the application's layout is structured using Dash and Bootstrap components.
- **[GRAPH.md](docs/GRAPH.md)**: Detailed documentation of `graph.py`, describing how the Cytoscape graph component is created and configured.
- **[HELPERS.md](docs/HELPERS.md)**: Explanation of `helpers.py`, detailing the utility functions for graph construction, database management, and search functionality.
- **[GRAPH_STATE.DB.md](docs/GRAPH_STATE.DB.md)**: Detailed explanation of `graph_state.db`, including how the application's state is persisted using SQLite.
- **[STYLES.CSS.md](docs/STYLES.CSS.md)**: Comprehensive description of `styles.css`, explaining how custom CSS styles are applied to the application.

## Customization

### Adding or Modifying Nodes

- **data.py**: Modify the `central_node`, `primary_nodes`, or `subnodes` dictionaries to add or change nodes and their relationships. Refer to [DATA.md](docs/DATA.md) for details.

### Changing Styles

- **assets/styles.css**: Update CSS styles to change the appearance of the application. See [STYLES.CSS.md](docs/STYLES.CSS.md) for guidance.
- **utils/helpers.py**: Modify the `create_stylesheet` function to change Cytoscape styles. Refer to [HELPERS.md](docs/HELPERS.md) for more information.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub if you'd like to contribute.

## License

This project is licensed under the [MIT License](LICENSE).

---
