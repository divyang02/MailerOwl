import os
import sys

sys.path.append(os.path.abspath('../../'))  # path to your django project

# Specify settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_sender.local_settings')

# Setup Django
import django
django.setup()


import pdoc

modules = ['apps.registration']
context = pdoc.Context()

modules = [pdoc.Module(mod, context=context)
           for mod in modules]
pdoc.link_inheritance(context)

def recursive_htmls(mod):
    yield mod.name, mod.html()
    for submod in mod.submodules():
        yield from recursive_htmls(submod)

for mod in modules:
    for module_name, html in recursive_htmls(mod):
        module_name  = module_name.split(".")[-1]
        with open(f"{module_name}.html", "w", encoding="utf8") as f:
            f.write(html)