from flask import Flask, jsonify, request
import json
from dotenv import load_dotenv
from os import getenv
import ipaddress
import re

load_dotenv()

app = Flask(__name__)


def validate_domain(domain: str) -> bool:
    """A pattern for domain name validation"""
    pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, domain):
        return True
    return False


def run_server():
    ip = getenv('ip')
    port = getenv('port')
    app.run(host=ip, port=port)


@app.route('/show_ip')
def show_ip() -> dict:
    """ Displays the list of whitelisted IP addresses. Reads and returns the IP addresses listed in the whitelist file."""
    with open('/opt/ddos-log-parser/new_parser/whitelist.conf', 'r+') as f:
        white_list = [line.strip() for line in f.readlines()]
    ip_dict = {}
    for i in range(len(white_list)):
        ip_dict[i] = white_list[i]

    return jsonify(ip_dict)


@app.route('/add_ip', methods=['GET'])
def add_ip_whitelist() -> dict:
    """Adds an IP address or subnet to the whitelist. Expects a query parameter 'ip' containing the IP address or subnet to add."""
    ip_to_add = request.args.get('ip')
    print('ip:', ip_to_add)
    if ip_to_add:
        try:
            ip_network = ipaddress.ip_network(ip_to_add, strict=False)
            with open('/opt/ddos-log-parser/new_parser/whitelist.conf', 'r') as f:
                existing_ips = f.readlines()
                existing_ips = [line.strip() for line in existing_ips]

            if str(ip_network) in existing_ips:
                return jsonify({'status': 'error', 'message': f'IP or subnet {ip_to_add} already exists in the white list'})

            ip_str = str(ip_network)
            if ip_str.endswith('/32'):
                ip_str = ip_str[:-3]
            if ip_str not in existing_ips:
                with open('/opt/ddos-log-parser/new_parser/whitelist.conf', 'a+') as f:
                    f.write(ip_str + '\n') 
                return jsonify({'status': 'success', 'message': f'IP or subnet {ip_to_add} added to the white list'})
            else:
                return jsonify({'status': 'error', 'message': f'{ip_str} in whitelist'})
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Invalid IP or subnet provided'})
    else:
        return jsonify({'status': 'error', 'message': 'No IP provided in the request'})



@app.route('/add_mail')
def add_mail() -> dict:
    """Adds an email domain to a configuration file after validating its format. Expects 'mail' as a query parameter."""
    mail_to_add = request.args.get('mail')
    if mail_to_add:
        if validate_domain(mail_to_add):
            with open('/opt/mail-ban-parser/domain.conf', 'r') as f:
                domains = [line.strip() for line in f.readlines()]
            if mail_to_add not in domains:
                with open('/opt/mail-ban-parser/domain.conf', 'a+') as f:
                    f.write('\n' + mail_to_add)
                return jsonify({'status': 'success', 'message': f'{mail_to_add} added to file domain.conf'})
            return jsonify({'status': 'error', 'message': f'{mail_to_add} already exists in domain.conf'})
        return jsonify({'status': 'error', 'message': 'Invalid domain format'})
    else:
        return jsonify({'status': 'error', 'message': 'No domain provided in the request'})


@app.route('/')
def search_json_logs() -> dict:
    """Returns data from a JSON log file related to a specific functionality."""
    with open('/opt/data_files/ftp_logs.json', 'r') as f:
        return json.load(f)


@app.route('/mail')
def search_json_mail():
    """Returns data from a JSON file related to mail banning functionality."""
    with open('/opt/data_files/mail_ban.json', 'r') as f:
        return json.load(f)


@app.route('/dock')
def available_endpoints() -> dict:
    """Displays available endpoints along with their URLs, methods, and function names."""
    endpoints_dict = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            endpoint = {
                'url': str(rule),
                'methods': sorted(rule.methods - {'HEAD', 'OPTIONS'}),
                'function': app.view_functions[rule.endpoint].__name__,
                'doc': app.view_functions[rule.endpoint].__doc__
            }
            endpoints_dict[rule.endpoint] = endpoint
    return jsonify(endpoints_dict)

if __name__ == '__main__':
    run_server()
