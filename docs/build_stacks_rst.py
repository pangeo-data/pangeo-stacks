import os
import json
import pathlib
import pprint
import re
import requests
import subprocess

import jinja2
from rstcloth.rstcloth import RstCloth


template_html = """    <div class="panel-group" id="accordion-{{ id }}">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h4 class="panel-title">
            <a data-toggle="collapse" data-parent="#accordion-{{ id }}" href="#collapse1-{{ id }}">
            conda list
            </a>
          </h4>
        </div>
        <div id="collapse1-{{ id }}" class="panel-collapse collapse">
          <div class="panel-body">
            <table class="table table-condensed table-hover">
            <tbody>
            <tr><td>Package</td><td>Version</td></tr>
           {% for key, value in conda_list.items() %}
             <tr><td>{{ key | e }}</td><td>{{ value | e }}</td></tr>
           {% endfor %}
            </tbody>
           </table>
          </div>
        </div>
      </div>
      <div class="panel panel-default">
        <div class="panel-heading">
          <h4 class="panel-title">
            <a data-toggle="collapse" data-parent="#accordion-{{ id }}" href="#collapse2-{{ id }}">
             metadata</a>
          </h4>
        </div>
        <div id="collapse2-{{ id }}" class="panel-collapse collapse">
          <div class="panel-body">
           <table class="table table-condensed table-hover">
            <tbody>
           {% for key, value in metadata.items() %}
             <tr><td>{{ key | e }}</td><td>{{ value | e }}</td></tr>
           {% endfor %}
            </tbody>
           </table>
          </div>
        </div>
      </div>
    </div>
"""
template = jinja2.Template(template_html)


# https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
def to_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s).lower()

def normalize_document_path(prefix_and_name, extension=''):
    if len(prefix_and_name)==0:
        return
    path = os.path.join(*[to_valid_filename(p) for p in prefix_and_name])
    return path + extension


def conda_json_to_version_dict(s):
    out = {}
    sdict = json.loads(s.decode())

    for package in sdict:
      out[package['name']] = package['version']

    return out


def docker_json_to_metadata_dict(s):
    out = {}
    keep = ['RepoTags', 'Created', 'DockerVersion', 'Architecture',
            'Os', 'Size']
    sdict = json.loads(s.decode())[0]
    for k, v in sdict.items():
        if k in keep:
            out[k] = v
    size = int(out['Size']) / 1e9
    out['Size'] = f'{size:.2f} GB'
    return out


class StacksRSTBuilder:

    def __init__(self, images, output_dir, actually_load=True):
        self.images = images
        self.output_dir = output_dir
        self.actually_load = actually_load

    def conda_list(self, image):
        # return "docker run ... conda list"
        args = [
            'docker', 'run', '-it',
            '--entrypoint=""',
            image,
            'conda', 'list', '--json']
        joined_args = " ".join(args)
        out = subprocess.check_output(joined_args, shell=True)
        out = conda_json_to_version_dict(out)
        return out

    def docker_inspect(self, image):
        # return "docker run ... conda list"
        args = ['docker', 'image', 'inspect', image]
        joined_args = " ".join(args)
        out = subprocess.check_output(joined_args, shell=True)
        out = docker_json_to_metadata_dict(out)
        return out

    def write_rst(self):
        document_path = normalize_document_path([self.output_dir] + ['images'],
                                                extension='.rst')
        print(document_path)
        d = RstCloth()

        d.title('Docker Images')
        d.newline()
        d.content('DockHub URL:')
        d.newline()
        d.codeblock('https://hub.docker.com/u/pangeo', language='html')
        d.newline()

        for image in self.images:
            d.h3(image)
            d.newline()

            conda_list = self.conda_list(image)

            metadata = {'URL': f'https://hub.docker.com/r/{image}'}
            metadata.update(self.docker_inspect(image))

            id = image.split('/')[1]

            html = template.render(id=id, conda_list=conda_list, metadata=metadata)
            d.directive('raw', arg='html', content=html)
            d.newline()

        d.write(document_path)


    def build(self):
        self.write_rst()


def main():
    images = [
        'pangeo/base-notebook', 'pangeo/pangeo-notebook',
        'pangeo/base-notebook-onbuild', 'pangeo/pangeo-notebook-onbuild',
        'pangeo/pangeo-esip'
    ]
    output_rst_dir = ''
    builder = StacksRSTBuilder(images, output_rst_dir, actually_load=True)
    builder.build()


if __name__ == "__main__":
    # execute only if run as a script
    main()
