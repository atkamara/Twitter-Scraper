# -*- coding: latin-1 -*-
from flask import current_app as app
import os,json

@app.template_filter('text_area_value')
def add_text(value,text):
	return value[:-12]+json.dumps(text, indent=1, sort_keys=False)+value[-12:]