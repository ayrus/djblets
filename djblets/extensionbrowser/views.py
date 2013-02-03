from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from djblets.extensionbrowser.forms import AddExtensionForm
import pkg_resources
from setuptools.command import easy_install


@staff_member_required
def add_extension(request, extension_manager,
                  template_name='extensionbrowser/extension_manager.html'):
    """View for adding extensions.

    Presents a view for inputing remote extension URLs and then
    the extension at the given resource is installed.
    """
    distribution_error = False
    install_error = False
    install_success = False
    error = None
    if request.method == 'POST':
        form = AddExtensionForm(request.POST)

        if form.is_valid():
            try:
                easy_install.main(["-U", request.POST['extension_url']])

                dist = pkg_resources.get_distribution(
                    request.POST['package_name'])
                dist.activate()
                pkg_resources.working_set.add(dist)

                extension_manager.load(True)

            except pkg_resources.DistributionNotFound:
            # Raised by pkg_resources, user likely entered the wrong name at
            # package_name.
                distribution_error = True

            except Exception, e:
            # Problem with install.
                install_error = True
                error = e

            if  not distribution_error and not install_error:
                # At this point, everything went okay with the installation.
                install_success = True

    else:
        form = AddExtensionForm()

    return render_to_response(template_name, RequestContext(request, {
            'distribution_error': distribution_error,
            'error': error,
            'form': form,
            'install_error': install_error,
            'install_success': install_success,
        }))
