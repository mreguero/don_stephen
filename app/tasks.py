import os
from django.template import loader
from django.core.files.base import ContentFile
from .models import Feature
from behave.runner_util import make_undefined_step_snippet

BASEPATH = os.path.dirname(__file__)

def gen_feature_file(feature_id):

    feature = Feature.objects.get(id=feature_id)
    template = loader.get_template('app/Feature/Base.feature')
    data_dict = {
        'description': feature.description,
        'finality': feature.finality,
        'who': feature.who,
        'purpose': feature.purpose, 
        'title': feature.scenario.all()[0].title,
        'given': feature.scenario.all()[0].given,
        'when': feature.scenario.all()[0].when,
        'then': feature.scenario.all()[0].then}

    
    c = ContentFile(content=template.render(data_dict))
    feature.ffile.save('{}.feature'.format(feature.id), c)


def make_test_funcs(steps, feature_id):

    filename = 'test_{}.py'.format(feature_id)
    with open(os.path.join('stephen_demo_repo', filename), 'w') as f:
        for step in steps:
            test_fun = make_undefined_step_snippet(step)
            f.write(test_fun)
    return filename

def add_to_repo(filename, feature):
    project_path = os.path.join(BASEPATH, '..')
    os.chdir(r'{}'.format(os.path.join(project_path, 'stephen_demo_repo')))
    os.system('git add {}'.format(filename))
    os.system('git commit -m "Added tests for feature {}"'.format(feature))
    os.system('git push origin master')
    os.chdir(r"{}".format(project_path))
