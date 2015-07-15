__author__ = 'Antonio'

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os, os.path
import time
import graphiteParser
import name_resolver_se
from pprint import pprint as pp


#Global variables.
GRAPHITE_DB = "../all_data_column.txt"
env = Environment(loader=FileSystemLoader('templates'))


class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index_start.html')
        return tmpl.render()


    @cherrypy.expose
    def gse_search(self):
        tmpl = env.get_template('index_gse_search.html')
        return tmpl.render()


    @cherrypy.expose
    def gse_result(self, queryParameters=None):
        tmpl = env.get_template('index_gse_result.html')

        #TODO: add chech for several spaces.
        queryParameters_list = queryParameters.strip().split(" ")
        metricsFound = graphiteParser.graphiteFileParser(GRAPHITE_DB, queryParameters_list)

        #pass queryParameters_list to the HTML page template. To prevent clear form after submit.
        return tmpl.render(metrics=metricsFound, params=queryParameters_list)


    @cherrypy.expose
    def scripted_dashboard(self, metricRadio=None):
        tmpl = env.get_template('index_grafana_scripted_dashboard.html')
        return tmpl.render(new_graph_url=metricRadio)


    @cherrypy.expose
    def name_resolver(self, server_name_form=""):
        tmpl = env.get_template('index_name_resolver.html')

        host_name_dict = {}

        if server_name_form:
            host_name_dict = name_resolver_se.resolve_server_name(server_name_form)

        return tmpl.render(server_name_form_to_tmpl=server_name_form, host_name_dict_to_tmpl=host_name_dict)


if __name__ == '__main__':

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    #TODO: need to place it to the conf.
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                            })

    # cherrypy.quickstart(Root(),'/', conf)
    cherrypy.quickstart(Root(),'/TAS/', conf)


