# callbacks.py

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import callback_context, html
import logging
import copy
from utils.helpers import perform_fuzzy_search, save_graph_state, load_graph_state

# Initialize logger for this module
logger = logging.getLogger(__name__)

def register_callbacks(app):
    """
    Registers all callbacks with the Dash app.

    Parameters:
        app (dash.Dash): The Dash application instance.
    """

    @app.callback(
        [
            Output('cytoscape-graph', 'elements'),
            Output('cytoscape-graph', 'zoom'),
            Output('cytoscape-graph', 'pan'),
            Output('node-info', 'children'),
            Output('rendered-notes', 'children'),
            Output('rendered-notes-section', 'style'),
            Output('node-notes', 'value'),
            Output('notes-section', 'style'),
            Output('save-alert', 'is_open'),
            Output('load-alert', 'is_open'),
            Output('note-save-alert', 'is_open')
        ],
        [
            Input('zoom-in', 'n_clicks'),
            Input('zoom-out', 'n_clicks'),
            Input('reset-zoom', 'n_clicks'),
            Input('load-state', 'n_clicks'),
            Input('save-state', 'n_clicks'),
            Input('save-note', 'n_clicks'),
            Input('node-search', 'value'),
            Input('cytoscape-graph', 'tapNodeData')
        ],
        [
            State('cytoscape-graph', 'elements'),
            State('cytoscape-graph', 'zoom'),
            State('cytoscape-graph', 'pan'),
            State('node-notes', 'value'),
            State('cytoscape-graph', 'tapNodeData')
        ]
    )
    def handle_interactions(
        zoom_in, zoom_out, reset_zoom, load_clicks, save_clicks, save_note_clicks,
        search_value, tapped_node_data,
        current_elements, current_zoom, current_pan, note_value, tapped_node_state
    ):
        """
        Handles zoom controls, loading/saving state, searching nodes, node taps, and saving notes.

        Returns:
            list: Updated elements, zoom, pan, node info, rendered notes, styles, and alert states.
        """
        ctx = callback_context

        if not ctx.triggered:
            # No action triggered; do not update
            raise PreventUpdate

        # Identify which input triggered the callback
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        logger.info(f"Combined Callback triggered by: {triggered_id}")

        # Initialize default outputs
        new_elements = copy.deepcopy(current_elements)
        new_zoom = current_zoom
        new_pan = current_pan
        node_info = "Click on a node to see details."
        rendered_notes = ''
        rendered_notes_style = {'display': 'none'}
        node_notes_value = ''
        notes_section_style = {'display': 'none'}
        save_alert = False
        load_alert = False
        note_save_alert = False

        ### Handling Zoom Controls ###
        if triggered_id in ['zoom-in', 'zoom-out', 'reset-zoom']:
            logger.info(f"Handling zoom action triggered by: {triggered_id}")

            zoom_factor = 0.2  # Define the amount by which to zoom in/out

            if triggered_id == 'zoom-in' and zoom_in:
                new_zoom += zoom_factor
                logger.debug(f"Zooming in: New Zoom Level = {new_zoom}")
            elif triggered_id == 'zoom-out' and zoom_out:
                new_zoom -= zoom_factor
                logger.debug(f"Zooming out: New Zoom Level = {new_zoom}")
            elif triggered_id == 'reset-zoom' and reset_zoom:
                new_zoom = 1.0  # Reset to default zoom level
                logger.debug("Resetting zoom to default level.")

            # Ensure zoom level stays within allowed limits
            new_zoom = max(0.5, min(new_zoom, 2.0))  # Example limits: 0.5 <= zoom <= 2.0
            logger.debug(f"Adjusted Zoom Level: {new_zoom}")

            return (
                new_elements,
                new_zoom,
                new_pan,
                node_info,
                rendered_notes,
                rendered_notes_style,
                node_notes_value,
                notes_section_style,
                save_alert,
                load_alert,
                note_save_alert
            )

        ### Handling Load State ###
        elif triggered_id == 'load-state' and load_clicks:
            logger.info("Load State button clicked. Loading graph state from database.")
            state = load_graph_state()
            if state:
                new_elements = state.get('elements', current_elements)
                new_zoom = state.get('zoom', 1.0)
                new_pan = state.get('pan', {'x': 0, 'y': 0})
                logger.debug(f"Loaded state - Zoom: {new_zoom}, Pan: {new_pan}")

                # Log node positions for debugging
                for elem in new_elements:
                    if 'source' not in elem['data'] and 'target' not in elem['data']:
                        position = elem.get('position', {'x': 0, 'y': 0})
                        logger.debug(f"Node ID: {elem['data']['id']}, Position: {position}")

                load_alert = True  # Open load alert
                logger.info("Graph state loaded successfully.")
            else:
                logger.warning("No state to load.")
                load_alert = False

            return (
                new_elements,
                new_zoom,
                new_pan,
                node_info,
                rendered_notes,
                rendered_notes_style,
                node_notes_value,
                notes_section_style,
                save_alert,
                load_alert,
                note_save_alert
            )

        ### Handling Save State ###
        elif triggered_id == 'save-state' and save_clicks:
            logger.info("Save State button clicked. Saving graph state to database.")
            state_to_save = {
                'elements': new_elements,
                'zoom': new_zoom,
                'pan': new_pan
            }
            success = save_graph_state(state_to_save)
            if success:
                save_alert = True  # Open save alert
                logger.info("Graph state saved successfully.")
            else:
                logger.error("Failed to save graph state.")
                save_alert = False

            return (
                new_elements,
                new_zoom,
                new_pan,
                node_info,
                rendered_notes,
                rendered_notes_style,
                node_notes_value,
                notes_section_style,
                save_alert,
                load_alert,
                note_save_alert
            )

        ### Handling Save Note ###
        elif triggered_id == 'save-note' and save_note_clicks:
            if tapped_node_state:
                node_id = tapped_node_state.get('id')
                # Update the note in the elements
                for elem in new_elements:
                    if elem['data'].get('id') == node_id:
                        elem['data']['notes'] = note_value  # Update the notes
                        logger.info(f"Note saved for node {node_id}.")
                        break
                else:
                    logger.warning(f"Node with ID {node_id} not found in elements.")
                note_save_alert = True
                # Update the rendered notes
                rendered_notes = note_value
                rendered_notes_style = {'display': 'block'} if note_value.strip() else {'display': 'none'}
                node_notes_value = note_value
                notes_section_style = {'display': 'block'}

                # Optionally, save the updated state
                state_to_save = {
                    'elements': new_elements,
                    'zoom': new_zoom,
                    'pan': new_pan
                }
                save_graph_state(state_to_save)
            else:
                logger.warning("Save Note clicked without selecting a node.")

            return (
                new_elements,
                new_zoom,
                new_pan,
                node_info,
                rendered_notes,
                rendered_notes_style,
                node_notes_value,
                notes_section_style,
                save_alert,
                load_alert,
                note_save_alert
            )

        ### Handling Search ###
        elif triggered_id == 'node-search':
            # Ensure that classes are updated for all nodes based on the current search
            try:
                # Remove 'highlighted' class from all nodes
                for elem in new_elements:
                    if 'classes' in elem:
                        classes = elem['classes'].split()
                        if 'highlighted' in classes:
                            classes.remove('highlighted')
                        elem['classes'] = ' '.join(classes)
                if not search_value:
                    logger.info("Empty search query: All nodes are visible.")
                    node_info = "Search cleared. All nodes are visible."
                else:
                    # Extract all node labels from the current graph elements
                    all_labels = [
                        elem['data']['label'] for elem in current_elements
                        if 'source' not in elem['data'] and 'target' not in elem['data']
                    ]
                    # Perform substring search to find matching labels
                    matching_labels = perform_fuzzy_search(search_value, all_labels)
                    logger.info(f"Search query: '{search_value}' | Matches: {matching_labels}")

                    if not matching_labels:
                        logger.info("No matching nodes found for the search query.")
                        node_info = "No matching nodes found."
                    else:
                        # Update 'classes' for each node based on whether it matches
                        for elem in new_elements:
                            if 'source' in elem['data'] and 'target' in elem['data']:
                                continue  # Skip edges
                            label = elem['data'].get('label', '')
                            if label in matching_labels:
                                # Add 'highlighted' class if not already present
                                classes = elem.get('classes', '').split()
                                if 'highlighted' not in classes:
                                    classes.append('highlighted')
                                elem['classes'] = ' '.join(classes)
                            else:
                                # Ensure 'highlighted' class is not present
                                classes = elem.get('classes', '').split()
                                if 'highlighted' in classes:
                                    classes.remove('highlighted')
                                elem['classes'] = ' '.join(classes)
                        node_info = "Matching nodes highlighted."

            except Exception as e:
                logger.error(f"Error during search callback: {e}")
                node_info = "An error occurred during the search."

            return (
                new_elements,
                new_zoom,
                new_pan,
                node_info,
                rendered_notes,
                rendered_notes_style,
                node_notes_value,
                notes_section_style,
                save_alert,
                load_alert,
                note_save_alert
            )

        ### Handling Node Tap ###
        elif triggered_id == 'cytoscape-graph':
            if tapped_node_data:
                try:
                    # Extract relevant data from the tapped node
                    label = tapped_node_data.get('label', 'No Label')
                    description = tapped_node_data.get('description', 'No description available.')
                    notes = tapped_node_data.get('notes', '')
                    logger.info(f"Node tapped: {label}")

                    # Create HTML content to display node information
                    node_info = html.Div([
                        html.H4(f"{label}"),
                        html.P(f"{description}")
                    ])

                    # Manage the visibility and content of the notes section
                    rendered_notes = notes
                    rendered_notes_style = {'display': 'block'} if notes.strip() else {'display': 'none'}
                    node_notes_value = notes
                    notes_section_style = {'display': 'block'}

                except Exception as e:
                    logger.error(f"Error during node tap callback: {e}")
                    node_info = "An error occurred while processing the node tap."
                    rendered_notes = ''
                    rendered_notes_style = {'display': 'none'}
                    node_notes_value = ''
                    notes_section_style = {'display': 'none'}

            return (
                new_elements,
                new_zoom,
                new_pan,
                node_info,
                rendered_notes,
                rendered_notes_style,
                node_notes_value,
                notes_section_style,
                save_alert,
                load_alert,
                note_save_alert
            )

        # If the trigger doesn't match expected inputs, prevent update
        raise PreventUpdate
