# Sending the weight

This project collects and sends the balance data to a remote server, logs errors and handles data transmission failures, storing the data locally for later transmission.

## Setup and Installation

### 1. Virtual Environment Setup

1. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
2. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

### 2. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the sample configuration file:
    ```bash
    cp storage/.env.dist storage/.env
    ```
2. Edit "storage/.env" to configure libra ports, API URLs, credentials, etc.
   ```bash
    nano storage/.env
    ```

### 4. Run the Application

Run the application using:

```bash
python src/main.py
```

## Data Transmission

### Send Data

The application sends libra data in the following JSON format:

```json
{
    "location_name": "location_name",
    "ok": true,
    "results": [
        {
            "date": "2025-06-09T10:00:00.006031",
            "weight": -1
        },
        {
            "date": "2025-06-09T10:00:01.006161",
            "weight": 10000000
        }
    ]
}
```

The authentication is handled via HTTP headers using the `Authorization` field:

```python
headers = {
    "Authorization": "Basic <base64-encoded-credentials>"
}
```

### Error Logging

If an error occurs during data transmission, it is logged locally and optionally sent to the server in the following format:

```json
{
    "location_name": "location_name",
    "ok": false,
    "error_message": "Error sending consumption",
    "exception": "Failed to connect to Modbus client.",
    "traceback": "....................."
}
```

## Notes

- Ensure `.env` is properly configured before running the application.
- Activate the virtual environment for any operations related to the project.
