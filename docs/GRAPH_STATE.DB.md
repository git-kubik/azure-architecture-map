# GRAPH_STATE.DB.md

## Overview of `graph_state.db`

The `graph_state.db` file is a SQLite database used by the Azure Architecture Map application to persist the state of the graph. This includes the positions of nodes, zoom levels, pan positions, and any custom notes added to the nodes by the user. By saving this state, the application can restore the graph to its previous configuration, providing a consistent user experience across sessions.

---

## Table of Contents

- [Purpose of `graph_state.db`](#purpose-of-graph_statedb)
- [Database Structure](#database-structure)
  - [1. Database Schema](#1-database-schema)
  - [2. Data Stored](#2-data-stored)
- [Detailed Explanation](#detailed-explanation)
  - [Initialization of the Database](#initialization-of-the-database)
  - [Saving Graph State](#saving-graph-state)
  - [Loading Graph State](#loading-graph-state)
- [Integration with the Application](#integration-with-the-application)
  - [Usage in `utils/helpers.py`](#usage-in-utilshelperspy)
  - [Callbacks and State Management](#callbacks-and-state-management)
- [Security Considerations](#security-considerations)
- [Backup and Maintenance](#backup-and-maintenance)
- [Extensibility](#extensibility)
- [Conclusion](#conclusion)

---

## Purpose of `graph_state.db`

- **State Persistence**: The primary purpose of `graph_state.db` is to store the current state of the graph, allowing users to save their configurations and restore them later.
- **User Experience**: By persisting node positions and notes, the application enhances the user experience by maintaining custom layouts and annotations.
- **Data Integrity**: Using a database ensures that the saved state is stored reliably and can be retrieved without data loss.

---

## Database Structure

### 1. Database Schema

The `graph_state.db` database contains a single table named `graph_state`. The schema of the table is as follows:

```sql
CREATE TABLE graph_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL
);
```

- **id**: An integer primary key that auto-increments. It uniquely identifies each saved state entry.
- **state**: A text field that stores the serialized JSON representation of the graph state.

### 2. Data Stored

The `state` field contains a JSON string that includes:

- **elements**: The list of graph elements (nodes and edges), including their positions and any custom data such as notes.
- **zoom**: The zoom level of the graph at the time of saving.
- **pan**: The pan position (x and y coordinates) of the graph at the time of saving.

---

## Detailed Explanation

### Initialization of the Database

- **Module**: The database interactions are handled in `utils/helpers.py`.
- **Initialization Function**: The `initialize_db()` function ensures that the `graph_state` table exists in the database.

```python
def initialize_db():
    """
    Initializes the SQLite database by creating the 'graph_state' table if it does not exist.
    """
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS graph_state (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    state TEXT NOT NULL
                )
            ''')
            conn.commit()
            logger.info("Database initialized and 'graph_state' table ensured.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
```

- **Execution**: This function is called when `utils/helpers.py` is imported, ensuring that the database is ready for use when the application starts.

### Saving Graph State

- **Function**: `save_graph_state(state)`
- **Purpose**: Serializes and saves the current graph state to the database.
- **Process**:
  - Converts the `state` dictionary to a JSON string.
  - Deletes any existing entries in the `graph_state` table to keep only the latest state.
  - Inserts the new state into the table.

```python
def save_graph_state(state):
    """
    Saves the graph state to the SQLite database.

    Parameters:
        state (dict): The state dictionary containing elements, zoom, and pan.

    Returns:
        bool: True if saved successfully, False otherwise.
    """
    try:
        state_json = json.dumps(state)
        logger.debug(f"Saving graph state: {state_json}")
        with get_db_connection() as conn:
            c = conn.cursor()
            # Remove existing state to maintain only the latest
            c.execute('DELETE FROM graph_state')
            # Insert new state
            c.execute('INSERT INTO graph_state (state) VALUES (?)', (state_json,))
            conn.commit()
        logger.info("Graph state successfully saved to the database.")
        return True
    except sqlite3.Error as e:
        logger.error(f"SQLite error while saving graph state: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while saving graph state: {e}")
        return False
```

- **Note**: Only one state is stored at a time, ensuring that the database size remains minimal.

### Loading Graph State

- **Function**: `load_graph_state()`
- **Purpose**: Retrieves the saved graph state from the database.
- **Process**:
  - Fetches the most recent entry from the `graph_state` table.
  - Parses the JSON string back into a Python dictionary.
  - Returns the state dictionary for use in restoring the graph.

```python
def load_graph_state():
    """
    Loads the graph state from the SQLite database.

    Returns:
        dict or None: The loaded state dictionary containing elements, zoom, and pan,
                      or None if no state is found.
    """
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            # Retrieve the latest graph state entry
            c.execute('SELECT state FROM graph_state ORDER BY id DESC LIMIT 1')
            row = c.fetchone()
            if row:
                state_json = row[0]
                state = json.loads(state_json)
                logger.info("Graph state successfully loaded from the database.")
                return state
            else:
                logger.warning("No graph state found in the database.")
                return None
    except sqlite3.Error as e:
        logger.error(f"SQLite error while loading graph state: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error while loading graph state: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while loading graph state: {e}")
        return None
```

- **Handling Missing State**: If no state is found, the function returns `None`, and the application can handle this case appropriately.

---

## Integration with the Application

### Usage in `utils/helpers.py`

- **Database Connection**: A context manager `get_db_connection()` is used to manage database connections safely.

```python
@contextmanager
def get_db_connection():
    """
    Context manager for SQLite database connection.

    Yields:
        sqlite3.Connection: The SQLite database connection object.
    """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        logger.debug(f"Connected to SQLite database at {DATABASE_FILE}")
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.debug("SQLite database connection closed.")
```

- **Functions**: The `save_graph_state` and `load_graph_state` functions are the primary interfaces for interacting with the database.

### Callbacks and State Management

- **Module**: `callbacks.py`
- **Saving State**:
  - When the user clicks the **"Save State"** button, the `save_graph_state` function is called with the current graph state.
  - The state includes elements, zoom level, and pan position.
- **Loading State**:
  - When the user clicks the **"Load State"** button, the `load_graph_state` function is called.
  - If a saved state exists, the graph is updated with the loaded elements, zoom, and pan.
- **Example in `callbacks.py`**:

```python
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
```

---

## Security Considerations

- **Local Storage**: The `graph_state.db` file is stored locally on the server where the application is running.
- **Data Sensitivity**:
  - The data stored includes user-added notes and graph configurations.
  - Ensure appropriate file permissions are set to prevent unauthorized access.
- **Encryption**:
  - If the application is deployed in a multi-user environment, consider implementing encryption or user-specific databases to protect data.
- **Database Locking**:
  - SQLite may lock the database file during write operations. Ensure that the application handles such scenarios, especially if multiple threads or processes might access the database concurrently.

---

## Backup and Maintenance

- **Backup**:
  - Regular backups of `graph_state.db` can prevent data loss in case of server failure.
  - Backups can be as simple as copying the file to a secure location.
- **Maintenance**:
  - Since the database only stores the latest state, it remains small in size.
  - Monitor the file size to ensure it doesn't grow unexpectedly.
- **Integrity Checks**:
  - Periodically verify the integrity of the database using SQLite's `PRAGMA integrity_check;` command.

---

## Extensibility

- **Additional Tables**:
  - If future requirements necessitate storing more data, additional tables can be added to `graph_state.db`.
- **Versioning**:
  - Implementing versioning of saved states can allow users to save multiple configurations.
  - This would require modifying the schema to handle multiple state entries per user or session.
- **Multi-User Support**:
  - In a shared environment, consider adding user identifiers to the schema to support personalized states.

---

## Conclusion

The `graph_state.db` SQLite database is a vital component of the Azure Architecture Map application, providing persistent storage for the graph's state. By leveraging a simple database with a straightforward schema, the application ensures that users can save their work and return to it later, enhancing usability and user experience.

Understanding the structure and usage of `graph_state.db` allows developers to:

- **Customize Persistence**: Modify how and what data is stored, such as adding versioning or user-specific states.
- **Enhance Security**: Implement measures to secure the data, especially in shared environments.
- **Extend Functionality**: Add new features that require data persistence, utilizing the existing database infrastructure.

---

## Additional Notes

- **SQLite Advantages**:
  - Lightweight and serverless, making it suitable for applications without heavy database requirements.
  - Stores the entire database in a single file, simplifying deployment and backups.
- **Thread Safety**:
  - SQLite connections are not inherently thread-safe. Ensure that database access is managed appropriately, especially in multi-threaded environments.
- **Data Serialization**:
  - The state is stored as a JSON string. Ensure that any changes to the structure of the state dictionary are compatible with the JSON format.

---

**By understanding `graph_state.db`, developers can effectively manage the persistent state of the application, ensuring that users have a seamless and consistent experience across sessions.**