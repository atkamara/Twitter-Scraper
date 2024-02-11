# -*- coding: latin-1 -*-
import json,os
from flask_wtf               import FlaskForm
from wtforms                 import (
                                    StringField,
                                    TextAreaField,
                                    SubmitField,
                                    DateField,
                                    IntegerField,
                                    SelectField,
                                    BooleanField,
                                    IntegerRangeField)

from wtforms.validators import DataRequired, ValidationError

def Jsonvalidator(form, field):
    '''
    Description(FR)
    ---------------
    Il s’agit d’une fonction permettant
     d’intercepter les erreurs de 
     structuration des json.
    '''
    try:
        json.loads(field.data or '')
    except ValueError as err:
        raise ValidationError('Please provide a valid Json file !')


class TWXTStorageForm(FlaskForm)    :
    TWXT_output                     = StringField("TWXT_output",[DataRequired()])# on ne vérifie pas si le path est autorisé
    submit                          = SubmitField("Submit")

class SearchForm(FlaskForm):
    query                           = StringField("Query",[DataRequired()])
    filters                         = StringField("Filters",[])
    start_date                      = DateField("Start Date",[DataRequired()])
    end_date                        = DateField("End Date",[DataRequired()])
    search_range                    = IntegerField("Search Range",[DataRequired()])
    recent                          = BooleanField("Recent")
    submit                          = SubmitField("Submit")

class WebdriverTimeoutForm(FlaskForm):
    search_bar                      = IntegerRangeField("Search Bar")
    recent                          = IntegerRangeField("Recent Stories")
    list_of_articles                = IntegerRangeField("List of articles")
    submit                          = SubmitField("Submit")


class WebdriverBrowserForm(FlaskForm):
    browser                         = SelectField("Browser",[DataRequired()],
                    choices         = [("Chrome", "Chrome"),("Firefox", "Firefox")],)
    headless                        = BooleanField("Headless")
    no_sandbox                      = BooleanField("No sandoxing")
    no_images                       = BooleanField("No images")
    hheight                         = IntegerRangeField("Height")
    wwidth                          = IntegerRangeField("Width")
    submit                          = SubmitField("Submit")

class WebdriverShakeForm(FlaskForm):
    json                            = TextAreaField("JSON",[Jsonvalidator])
    submit                          = SubmitField("Submit")

class CssForm(FlaskForm):
    json                            = TextAreaField("JSON",[Jsonvalidator])
    submit                          = SubmitField("Submit")


forms_names_objects                 = {

               'TWXTStorage'        :   [TWXTStorageForm,{'endpoint':'Storage'}],
               'Search'             :   [SearchForm,{'endpoint':'Search'}],
               'Timeout'            :   [WebdriverTimeoutForm,{'endpoint':'Webdriver','submitted_form_name':'index'}],
               'Browser'            :   [WebdriverBrowserForm,{'endpoint':'Webdriver','submitted_form_name':'index'}],
               'Shake'              :   [WebdriverShakeForm,{'endpoint':'Webdriver','submitted_form_name':'index'}],
               'Css'                :   [CssForm,{'endpoint':'Css'}]}
