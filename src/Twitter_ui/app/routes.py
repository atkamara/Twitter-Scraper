# -*- coding: latin-1 -*-
from .utils         import *
from .filters       import *
from .forms         import forms_names_objects



@app.route("/")
def home():
    return render_template("Index.html",
                                 title        = "Home")


@app.route("/Storage",
                                methods       = ["GET", "POST"])
def Storage():
    forms_names                               = ["TWXTStorage"]
    Storage_route                             = route_handler(
                                  forms_names = forms_names,
                                template_name = "Storage.html",
                                        title = "Storage",
                          forms_names_objects = forms_names_objects)
    Storage_route.get_forms()
    return  Storage_route.handle_requests(
                                       config = True)


@app.route("/Search",
                                methods       = ["GET", "POST"])
def Search():
    forms_names                               = ["Search"]
    Search_route                              = route_handler(
                                  forms_names = forms_names,
                                template_name = "Search.html",
                                        title = "Search",
                          forms_names_objects = forms_names_objects)
    Search_route.get_forms()
    return Search_route.handle_requests()


@app.route("/Webdriver/<submitted_form_name>", 
                                methods       = ["GET","POST"])
def Webdriver(submitted_form_name='index'):
    forms_names                               = ["Timeout","Browser","Shake"]
    Webdriver_route                           = route_handler(
                                  forms_names = forms_names,
                                template_name = "Webdriver.html",
                                        title = "Webdriver",
                          forms_names_objects = forms_names_objects)
    Webdriver_route.get_forms()
    select_browser_first                      = [Webdriver_route.forms[1][2]['browser']]+list(map(lambda x :x[0],Webdriver_route.forms[1][1].browser.choices))
    Webdriver_route.\
        forms[1][1].browser.choices           = get_unique_keep_order(select_browser_first)
    return Webdriver_route.handle_requests(
                        submitted_form_name   = submitted_form_name)


@app.route("/Css",
                                methods       = ["GET", "POST"])
def Css():
    forms_names                               = ["Css"]
    Css_route                                 = route_handler(
                                  forms_names = forms_names,
                                template_name = "Css.html",
                                        title = "Css",
                          forms_names_objects = forms_names_objects)
    Css_route.get_forms()
    return Css_route.handle_requests()






@app.route("/success/<form_name>", 
                                methods       = ["GET", "POST"])
def success(form_name):
    form_sucess_object                        = {
                            'name'            : form_name,
                            'path'            : os.path.join(app.config['OUTPUT_FOLDER'], form_name+'.json'),
                            'url'             : url_for(**forms_names_objects[form_name][1] )
                            }
    return render_template(
                                                "success.html",
                          form_sucess_object  = form_sucess_object)