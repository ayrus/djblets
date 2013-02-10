import pkg_resources
from setuptools.command import easy_install
import simplejson as json
from urllib import urlencode
from urllib2 import URLError, Request, urlopen

class Extension(object):
    """A class for depicting an extension from the store.

    Each extension retrieved from querying the store is instantiated
    as an instance of this class, which is eventually used to display
    a list on the view. An extension can be installed with a member 
    function.
    """
    def __init__(self, name, description, version, author, installed):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.installed = installed

    '''def install_extension(self, extension_manager):
        """ Install an extension.

        Install the extension invovled with this instance of the class.
        Method expects the global extension manager. Exceptions raised
        (if any) have to be caught by the caller.
        """
        easy_install.main(["-U", self.install_url])

        # Update the entry points.
        dist = pkg_resources.get_distribution(
            self.package_name)
        dist.activate()
        pkg_resources.working_set.add(dist)

        # Refresh the extension manager.
        extension_manager.load(True)'''

    def get_short_description(self):
        if(len(self.description) > 258):
            return self.description[:258] + '...'

        return self.description

    def set_installed(self, installed):
        self.installed = installed

class ExtensionStoreQuery(object):
    """Allows querying the extension store for a possible list of extensions.

    A supported extension store can be queried (with or without parameters)
    for a list of extensions available. A JSON response is expected which is
    parsed into a dictionary of Extension class objects.
    """

    def __init__(self, store_url, extension_manager):
        self.store_url = store_url
        self.installed_extensions = [ext.name for ext in extension_manager._entrypoint_iterator()]

    def _query(self, params):
        """Query the store.

        Perform the actual HTTP request to the store with parameters (if any).
        """
        request_url = self.store_url

        if params:
            url_params = urlencode(params)
            request_url = self.store_url + '?' + url_params

        print request_url

        request = Request(request_url)

        try:
            response = urlopen(request)

        except URLError as e:
            # TODO: Handle
            pass

        else:
            return json.loads(response.read())

    def populate_extensions(self, params):
        """Query and populate the result of extensions.

        Query for a list of extensions with the given params against the 
        extension store and return a dictionary of Extension class objects.
        Extension IDs are keys mapped to coressponding Extension objects.
        """
        response = self._query(params)
        extlist = {}
        extensions = response['extensions']

        for ext in extensions:
            installed = ext['package_name'] in self.installed_extensions
            extlist[ext['id']] = Extension(ext['name'], ext['description'],
                                           ext['version'], ext['author'],
                                           installed)

        return extlist
