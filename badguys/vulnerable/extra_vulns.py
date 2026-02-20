"""
Additional vulnerability examples for security demonstration.
WARNING: This code contains intentional security vulnerabilities.
DO NOT use in production!
"""
import hashlib
import os
import pickle
import subprocess
import yaml


def unsafe_yaml_load(user_input):
    """Vulnerable to arbitrary code execution via YAML deserialization."""
    return yaml.load(user_input)


def unsafe_pickle_load(data):
    """Vulnerable to arbitrary code execution via pickle deserialization."""
    return pickle.loads(data)


def command_injection(user_input):
    """Vulnerable to OS command injection."""
    os.system("echo " + user_input)
    subprocess.call(user_input, shell=True)


def weak_password_hash(password):
    """Uses weak MD5 hashing for passwords."""
    return hashlib.md5(password.encode()).hexdigest()


def hardcoded_credentials():
    """Contains hardcoded secrets."""
    api_key = "sk_live_abcdef123456789"
    db_password = "admin123"
    secret_token = "supersecrettoken2024"
    return {
        "api_key": api_key,
        "password": db_password,
        "token": secret_token
    }


def sql_injection_example(user_id):
    """Vulnerable to SQL injection."""
    query = "SELECT * FROM users WHERE id = " + user_id
    return query


def path_traversal(filename):
    """Vulnerable to path traversal attacks."""
    base_dir = "/var/www/uploads/"
    file_path = base_dir + filename
    with open(file_path, 'r') as f:
        return f.read()


def insecure_random():
    """Uses insecure random number generation."""
    import random
    return random.randint(0, 999999)


def eval_user_input(expression):
    """Vulnerable to code injection via eval."""
    return eval(expression)


def insecure_deserialization(serialized_data):
    """Multiple deserialization vulnerabilities."""
    import marshal
    return marshal.loads(serialized_data)


def xxe_vulnerable(xml_string):
    """Vulnerable to XML External Entity (XXE) attacks."""
    from xml.etree.ElementTree import fromstring
    return fromstring(xml_string)


def ssrf_vulnerable(url):
    """Vulnerable to Server-Side Request Forgery."""
    import requests
    return requests.get(url).text


def insecure_temp_file():
    """Creates predictable temporary files."""
    import tempfile
    tmp = tempfile.mktemp()
    with open(tmp, 'w') as f:
        f.write("sensitive data")
    return tmp


def debug_enabled():
    """Exposes debug information."""
    DEBUG = True
    SECRET_KEY = "django-insecure-key-for-development-only"
    return {"debug": DEBUG, "key": SECRET_KEY}
