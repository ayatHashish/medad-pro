import requests


class Video:
    def __init__(self):
        
        self.url = "https://video-agent.8x8.com/api/v1/tokens"
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "authorization": "Bearer {Ep8rwFxMqMWNOfnI9HfCvs9bD9lMDHTCNcDKl6d1Q}"
        }

    def getToken(self):
        response = requests.post(self.url, headers=self.headers)

        # Check the response
        if response.status_code == 200:
            # Successful request
            data = response.json()
            # Process the response data here
            print("Token:", data.get('token'))
            return data
        else:
            print("Error:", response.status_code)
            print("Response:", response.text)
            return False
