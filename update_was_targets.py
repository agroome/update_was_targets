import os
import requests
from collections import defaultdict
from tenable.io import TenableIO
from dotenv import load_dotenv
from typing import Generator, Optional, Union
from pprint import pprint

load_dotenv()

tio = TenableIO()

access_key = os.getenv('TIO_ACCESS_KEY')
secret_key = os.getenv('TIO_SECRET_KEY')

request_headers = {
    'X-ApiKeys': f'accessKey={os.getenv("TIO_ACCESS_KEY")}; secretKey={os.getenv("TIO_SECRET_KEY")}',
    'Accept': 'application/json',
    'Content-type': 'application/json'
}


def export_assets(category: str, value: Optional[str] = None) -> Generator[dict, None, None]:
    '''Generator that yields a dict containing config_name and asset given tag category and value'''
    for asset in tio.exports.assets():
        for tag in asset['tags']:
            if tag['key'] == category: # and (tag['value'] == value or tag['value'] is None):
                yield {
                    'config_name': tag['value'],
                    'asset': asset
                }


def get_scan_config(name: str) -> Union[dict, None]:
    '''Search for a scan config with the given name return None if not found.'''

    # documented endpoint: https://developer.tenable.com/reference/was-v2-config-search
    response = requests.post('https://cloud.tenable.com/was/v2/configs/search', headers=request_headers, json={
      "field": "configs.name",
      "operator": "eq",
      "value": name
    })
    results = response.json()['items']
    if results:
        return results[0]


def build_targets(tag_category: str, tag_value: Optional[str] = None) -> dict:
    '''Build a dict of config_name: [target1, target2, ...].'''
    targets = defaultdict(list)
    for result in export_assets(tag_category):
        # use first entry in fqdns if it exists, otherwise first ipv4s
        addresses = result['asset']['fqdns'] or result['asset']['ipv4s']
        address = addresses[0]
        target = f'https://{address}'
        print(f'adding {target} to {result["config_name"]}')
        # add the url to the list of targets for given config_name
        targets[result['config_name']].append(target)
    return dict(targets)


def main():
    tag_category = 'web-app-target'
    for config_name, urls in build_targets(tag_category).items():
        # get config with name
        config = get_scan_config(config_name)
        config_id = config['config_id']

        pprint(config)
        
        # get config details
        # endpoint docs: https://developer.tenable.com/reference/was-v2-config-details
        response = requests.get(f'https://cloud.tenable.com/was/v2/configs/{config_id}', headers=request_headers)
        config_details = response.json()
        
        # update config 
        # endpoint docs: https://developer.tenable.com/reference/was-v2-config-upsert
        update_url = f"https://cloud.tenable.com/was/v2/configs/{config_id}"
        payload = {
            "targets": urls,
            "name": config_name,
            "description": config_details['description'],
            "folder_id": config_details['folder'],
            "owner_id": config_details['owner_id'],
            "template_id": config_details['template_id'],
            "user_template_id": config_details['user_template_id'],
            "scanner_id": config_details['scanner_id'],
            "schedule": config_details['schedule'],
            "notifications": config_details['notifications'],
            "permissions": config_details['permissions'],
            "settings": config_details['settings'],
        }
        print(f'updating {config_name}')
        for url in urls:
            print(f'   {url}')
        response = requests.put(update_url, json=payload, headers=request_headers)
        print(f'status: {response.status_code}: {response.reason}\n')
        
        
if __name__ == '__main__':
    main()       