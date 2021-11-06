import os

def get_template(name: str):
    template_path = os.path.join(os.getcwd(), name)
    
    if os.path.exists(template_path):
        with open(template_path, 'r') as template:
            template_lines = template.readlines()
            
        return "".join(template_lines)
    else:
        return ""