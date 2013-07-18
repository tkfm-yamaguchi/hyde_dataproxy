# coding: utf-8

from hyde.model import Expando
from hyde.plugin import Plugin
from fswrap import FS, File

from glob import glob
from jinja2 import Template
from contextlib import contextmanager
import yaml


class DataproxyData(Expando):
    """
    represents data for data proxy
    """
    @classmethod
    def FromDataPathes(klass, datapathes):
        expanded_pathes = glob(FS(datapathes).fully_expanded_path)
        return [klass(datapath) for datapath in expanded_pathes]

    def __init__(self, data_file):
        with open(data_file, "r") as f:
            self.__data = yaml.load(f.read())

        super(DataproxyData, self).__init__(self.__data)
        self.__data_file = File(data_file)

    @property
    def data_file(self):
        return self.__data_file


class DataproxySource(Expando):
    """
    represents template for data proxy
    """
    def __init__(self, site_config, source_config):
        def combine_path(parent, leaf):
            return FS.file_or_folder(parent.child(leaf))

        super(DataproxySource, self).__init__({
            "template": combine_path(site_config.content_root_path, source_config.template),
            "filename": combine_path(site_config.deploy_root_path,  source_config.filename),
            "dataprefix": source_config.dataprefix
            })


class Dataproxy(object):
    def __init__(self, source, data):
        super(Dataproxy, self).__init__()
        self.data = data
        self.source = source
        self._filename_ = None

    @property
    def filename(self):
        if self._filename_ is None:
            self._filename_ = self._generate_filename_()
        return self._filename_

    def _generate_filename_(self):
        return FS.file_or_folder(
                Template(self.source.filename.path).render(self.data))

    def generate_page(self):
        """
        OBSOLETED
        """
        with open(self.source.template, "r") as ft:
            with open(self.filename, "w") as fw:
                fw.write(Template(ft.read()).render({self.source.dataprefix: self.data}))


class DataproxyPlugin(Plugin):
    def __init__(self, site):
        super(DataproxyPlugin, self).__init__(site)
        self.proxies = []

    def begin_site(self):
        """
        Retrieve proxy configurations and store it.
        """

        if not hasattr(self.site.config, 'proxies'):
            return    # nothing to do

        site_config = self.site.config
        proxy_config = site_config.proxies

        self.proxy_data = DataproxyData.FromDataPathes(proxy_config.data.path)
        self.proxy_sources = [DataproxySource(site_config, source_config)
                                    for source_config
                                        in proxy_config.sources]

        for data in self.proxy_data:
            for source in self.proxy_sources:
                self.proxies.append(Dataproxy(source, data))

    def begin_node(self, node):
        """
        Remove template's resource from nodes and add data resource.
        """

        if not node.__class__.__name__ == "RootNode":
            return

        self.remove_templates_from_node(node)
        self.add_data_resources_to_node(node)

    def remove_templates_from_node(self, root_node):
        for source in self.proxy_sources:
            resource = root_node.resource_from_path(source.template)
            node = resource.node
            node.resources.remove(resource)

    def add_data_resources_to_node(self, root_node):
        with self.suppress_duplication_checker(root_node) as root_node:
            for proxy in self.proxies:
                resource = root_node.add_resource(proxy.source.template)
                setattr(resource, proxy.source.dataprefix, proxy.data)
                setattr(resource, "data_file", proxy.data.data_file)
                setattr(resource, "nocaches", True)

                if not hasattr(resource, "depends"):
                    setattr(resource, "depends", [])
                resource.depends.append(proxy.data.data_file)

                resource.set_relative_deploy_path(
                        proxy.filename.get_relative_path(
                            self.site.config.deploy_root_path
                            )
                        )

    @contextmanager
    def suppress_duplication_checker(self, node):
        org_func = node.resource_from_path
        node.resource_from_path = lambda path: None
        yield node
        node.resource_from_path = org_func

    def append_data_to_template_resource(self, node):
        """
        XXX : evation, remove me.
        """
        for source in self.proxy_sources:
            resource = node.resource_from_path(source.template)
            setattr(resource, source.dataprefix, self.proxy_data[0])

