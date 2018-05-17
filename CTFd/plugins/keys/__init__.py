from CTFd.plugins import register_plugin_assets_directory

import re
import string
import hmac
import base64
from aes import prpcrypt


class BaseKey(object):
    id = None
    name = None
    templates = {}

    @staticmethod
    def compare(self, saved, provided, teaminfo=None):
        return True


class CTFdStaticKey(BaseKey):
    id = 0
    name = "static"
    templates = {  # Nunjucks templates used for key editing & viewing
        'create': '/plugins/keys/assets/static/create-static-modal.njk',
        'update': '/plugins/keys/assets/static/edit-static-modal.njk',
    }

    @staticmethod
    def compare(saved, provided, teaminfo=None):
        if len(saved) != len(provided):
            return False
        result = 0
        for x, y in zip(saved, provided):
            result |= ord(x) ^ ord(y)
        return result == 0


class CTFdRegexKey(BaseKey):
    id = 1
    name = "regex"
    templates = {  # Nunjucks templates used for key editing & viewing
        'create': '/plugins/keys/assets/regex/create-regex-modal.njk',
        'update': '/plugins/keys/assets/regex/edit-regex-modal.njk',
    }

    @staticmethod
    def compare(saved, provided, teaminfo=None):
        res = re.match(saved, provided, re.IGNORECASE)
        return res and res.group() == provided

class CTFdDynamicKey(BaseKey):
    id = 2
    name = "dynamic"
    templates = {  # Nunjucks templates used for key editing & viewing
        'create': '/plugins/keys/assets/dynamic/create-dynamic-modal.njk',
        'update': '/plugins/keys/assets/dynamic/edit-dynamic-modal.njk',
    }

    @staticmethod
    def compare(saved, provided, teaminfo=None):
        pc = prpcrypt(teaminfo[-32:])
        try:
		decrypted = pc.decrypt(provided)
	except Exception:
    		return False
        if len(saved) != len(decrypted):
            return False
        result = 0
        for x, y in zip(saved, decrypted):
            result |= ord(x) ^ ord(y)
        return result == 0


KEY_CLASSES = {
    'static': CTFdStaticKey,
    'regex': CTFdRegexKey,
    'dynamic': CTFdDynamicKey
}


def get_key_class(class_id):
    cls = KEY_CLASSES.get(class_id)
    if cls is None:
        raise KeyError
    return cls


def load(app):
    register_plugin_assets_directory(app, base_path='/plugins/keys/assets/')
