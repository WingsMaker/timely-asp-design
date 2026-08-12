import os
import requests

DATAROBOT_API_KEY = os.getenv("DATAROBOT_API_KEY")
DATAROBOT_URL = os.getenv("DATAROBOT_URL", "https://app.datarobot.com/api/v2")

class DataRobotClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or DATAROBOT_API_KEY
        self.base_url = base_url or DATAROBOT_URL
        if not self.api_key:
            raise ValueError("DATAROBOT_API_KEY is required")

    def predict(self, deployment_id: str, data_payload: list):
        """Call DataRobot deployment for predictions.
        deployment_id: the DataRobot deployment id (string)
        data_payload: list of row dicts matching the training schema
        Returns parsed JSON response.
        """
        url = f"{self.base_url}/deployments/{deployment_id}/predictions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(url, headers=headers, json={"data": data_payload})
        resp.raise_for_status()
        return resp.json()
