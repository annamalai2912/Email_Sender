import json
import os

TEMPLATE_FILE = 'templates.json'

class EmailTemplateManager:
    def __init__(self):
        self.templates = self.load_templates()

    def load_templates(self):
        if os.path.exists(TEMPLATE_FILE):
            with open(TEMPLATE_FILE, 'r') as file:
                return json.load(file)
        return {}

    def save_templates(self):
        with open(TEMPLATE_FILE, 'w') as file:
            json.dump(self.templates, file)

    def add_template(self, name, content):
        self.templates[name] = content
        self.save_templates()

    def get_template(self, name):
        return self.templates.get(name, "")
