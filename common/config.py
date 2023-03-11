import json


class Config:
    def __int__(self, file_path="instaloader.json"):
        self.file_path = file_path
        # Add path checking
        if file_path:
            self.json = json.load(fp=self.file_path)

    def get_telegram_token(self):
        return self.get_telegram_config()['token']

    def get_instagram_config(self):
        return self.json['instagram']

    def get_telegram_config(self):
        return self.json['telegram']

    def get_instaloader_config(self):
        return self.json['instaloader']

    def get_instaloader_param(self, param: str):
        return self.get_instaloader_config()[param]

    def get_custom_node(self, node_name):
        return self.json[node_name]
