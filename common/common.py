import os


def site_name(http_link: str):
    if http_link.startswith('http'):
        full_site_name = http_link.split('/')[2]
        name = full_site_name.split('.')[1]
        return full_site_name.lower(), name.lower()
    else:
        return None


def file_list(path: str):
    return os.listdir('/Users/Admin/Example')
