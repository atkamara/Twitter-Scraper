# -*- coding: latin-1 -*-
import os,json,datetime
from flask          import current_app as app
from flask          import (redirect, 
                            render_template, 
                            url_for,
                            flash)

ENV_VARS                                          = {'TWXT_output' : 'OUTPUT_FOLDER'}

def default_parser_for_json(value):
    '''
    Description(FR):
    ------------
    Permet d'intercepter les objets datatime
    et de les convertire au format iso YYYY-MM-DD

    Parameters
    ----------
    value : string, integer, float or datetime object

    Return
    ------
    str

    '''
    if isinstance(value, (datetime.date,
                              datetime.datetime)):
        value                                    = value.isoformat()
    return value
read_json_file                                   = lambda folder,name: json.loads(open(os.path.join(folder, name+'.json') ).read())
write_json_file                                  = lambda res,folder,name: json.dump(res,open(os.path.join(os.path.join(folder, name+'.json') ),'w+'), indent=1,  default=default_parser_for_json)    

def get_unique_keep_order(seq):
    '''
    Description(FR):
    -----------
    Permet de retrouver les éléments uniques
    d'une liste tout en conservant l'order initial

    Parameters:
    ----------
    seq: iterable

    Returns:
    -------
    list of unique values

    '''
    seen                      = set()
    return [ x 
            for x in seq 
            if not (x in seen or seen.add(x))]
def get_form_output(form):
    '''
    Description(FR):
    -----------
    Cette fonction permet de restituer un dictionnaire contenant le résultat du formulaire. Elle gère deux cas:
        * Si aucun champ json n’a été renseigné, elle récupère tous les couples (clé,valeur) sauf ceux dont la clé est “submit” ou “csrf_token”
        * Sinon, le json est directement chargé depuis la clé json

    Parameters:
    ----------
    form: dict

    Returns:
    -------
    dict

    '''
    return {k:v for
                k,v in form.data.items() 
                if k not in [
                'submit',
                'csrf_token']
                 } if 'json' not in \
                 form.data else json.loads(
                    form.data['json'])
def get_forms_display_data(forms_names,
                            forms_names_objects):
    '''
    Description(FR):
    ---------------
    Permet de retrouver les données à afficher
    Elle retourne un liste d'objets avec 3 élément

    Parameters:
    -----------
    forms_names : a list of form names index
    forms_names_objects : a dictionnary

    Returns:
    -------
    Iterable with[ [form_name,FlaskForm,json] ...]


    '''
    main_folder,default_folder                  = [app.config['DEFAULT_FOLDER']]*2 # les deux réportoire sont les mêmes par défaut
    if 'OUTPUT_FOLDER' in app.config            : main_folder = app.config['OUTPUT_FOLDER']
    #permet de vérifier l'existence d'un fichier pour le formulaire
    form_available_in_main                      = lambda form_name : os.path.isfile(os.path.join(main_folder, form_name+'.json'))
    #permet la lecture du fichier s'il est dans main sinon dans le défaut
    read_folder                                 = lambda form_name : main_folder if form_available_in_main(form_name) else default_folder

    res                                         = [[ 
                                                     form_name,
                                                     forms_names_objects[form_name][0](),
                                                     read_json_file(read_folder(form_name),form_name) ]

                                                    for form_name in forms_names ]
    return res
class route_handler:
    '''
    Description(FR):
    ----------------
    Il s’agit d’une classe qui joue un rôle central dans l’application. 
    Elle permet de gérer les requêtes sur le site avec la méthode handle_requests. 
    Lorsqu’un formulaire est soumis, l’action de validation est effectuée au niveau de cette fonction. 
    Une fois validé, les données du formulaire  sont récupérées et stockées par cette même fonction qui par la suite redirige vers la page de réussite.

    Parameters:
    ----------
    forms_names: [string]
    template_name: html file name in template folder
    title: string
    forms_names_objects: a dictionnary

    '''
    def __init__(self,
                                                    forms_names,
                                                    template_name,
                                                    title,
                                                    forms_names_objects):
        self.forms_names                          = forms_names
        self.template_name                        = template_name
        self.title                                = title
        self.forms_names_objects                  = forms_names_objects
    def get_forms(self):
        self.forms                                = get_forms_display_data(
                                                    self.forms_names,
                                                    self.forms_names_objects)
    def handle_requests(self,
                            submitted_form_name   = None,
                                        config    = False
                                                 ):
        global_erros                              = []
        forms_to_validate                         = self.forms
        if submitted_form_name :
            forms_to_validate                     = list(filter(lambda f : f[0]==submitted_form_name,forms_to_validate))
        for form in forms_to_validate               :
                if form[1].validate_on_submit()      :
                    output                            = get_form_output(form[1])
                    if  config :
                        for var in ENV_VARS.keys()    :
                            if var in output          :
                                app.config[
                                ENV_VARS[var]]        = output[var]
                    if 'OUTPUT_FOLDER' in app.config:
                        os.makedirs(
                                                       app.config['OUTPUT_FOLDER'],
                                       exist_ok      = True)
                        write_json_file(                    output,
                                                            app.config['OUTPUT_FOLDER'],
                                                            form[0])
                        return redirect(url_for("success", 
                                            form_name = form[0]))
                    else : global_erros.append('''
                        Submission Failed !<br>Please \
                        You must set storage path <a href="\
                        /Storage">Here .</a> ''')
        return render_template(
                                                    self.template_name,
                                    title         = self.title,
                                global_erros      = global_erros,
                                                    **{form[0]+'Form'         :form[1] for form in self.forms},
                                                    **{form[0]+'_default_json':form[2] for form in self.forms})