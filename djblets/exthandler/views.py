from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from setuptools.command import easy_install
import pkg_resources

from djblets.exthandler.forms import AddExtensionForm


@staff_member_required
def add_extension(request, extension_manager,
                  template_name='exthandler/extension_manager.html'):

    if request.method == 'POST':

        form = AddExtensionForm(request.POST)

        if form.is_valid():

            user_message = False

            try:

                easy_install.main(["-U", request.POST['extension_URL']])

                dist = pkg_resources.get_distribution(
                    request.POST['package_name'])

                dist.activate()

                pkg_resources.working_set.add(dist)

                extension_manager.load(True)

            # Raised by pkg_resources, user likely entered the wrong name at
            # package_name.
            except pkg_resources.DistributionNotFound:

                user_message = "An error occurred: package name " + \
                    "does not match the resource downloaded."

                return render_to_response(template_name, locals(),
                                          context_instance=RequestContext(request))

            # Problem with install.
            except Exception, e:

                user_message = "An error occured: " + str(e)

                return render_to_response(template_name, locals(),
                                          context_instance=RequestContext(request))

            # At this point, everything went okay with the installation.
            user_message = 1

            return render_to_response(template_name, locals(),
                                      context_instance=RequestContext(request))

    else:

        form = AddExtensionForm()

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
