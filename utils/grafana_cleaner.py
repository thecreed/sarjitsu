#!/usr/bin/python

import json
import re
import requests
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class config(object):
    base_url = "http://localhost:9602"
    search_url = "%s/api/search" % base_url
    delete_url = "%s/api/dashboards/{grafana.uri}" % base_url
    api_key= "Bearer eyJrIjoieVViTUlxT0FUa0p6Z2VCSms1WTAwcnAzVnRmWE5TSVMiLCJuIjoiYWRtaW4iLCJpZCI6MX0="

    headers = {
        "Accept" : "application/json",
        "Authorization" : api_key
    }

    def get_delete_uri(self,**kwargs):
        self.uri = kwargs['uri']
        return self.delete_url.format(grafana=self)


class Grafana():

    def __init__(self):
        self.conf = config()

    def get_all_dashboards(self):
        logging.debug("getting dashboards from grafana: %s" % self.conf.search_url)
        r = requests.get(self.conf.search_url , headers=self.conf.headers )
        if r.status_code <> 200:
            logging.error("Error search api,"
                          "code: {r.status_code}".format(r))

        logging.debug("return text: {ret.text}".format(ret=r))
        return json.loads(r.text)


    def  delete_multiple_dashboards(self,regex_str):
        for dashboard in self.get_all_dashboards():
            if re.match(regex_str,dashboard['uri']):
                logging.debug("found matching dashboard {}".format(dashboard['uri']))
                url = self.conf.get_delete_uri(uri=dashboard["uri"])
                logging.debug("deleting uri {}".format(url))
                r = requests.delete(url, headers=self.conf.headers)



if __name__ == "__main__":
    gr = Grafana()
    gr.delete_multiple_dashboards('.*(bi-|DevOps-).*')

