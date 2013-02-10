from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from djblets.extensionbrowser.base import ExtensionStoreQuery
from djblets.extensionbrowser.forms import SearchForm

@staff_member_required
def browse_extensions(request, extension_manager,
                    template_name='extensionbrowser/extension_browser.html'):
    results = None

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            #The store URL will later be moved to a settings page.
            store = ExtensionStoreQuery("http://andromeda.ayrus.net/test.html", 
                extension_manager)
            results = store.populate_extensions(request.POST);

    else:
        form = SearchForm()

    return render_to_response(template_name, RequestContext(request, {
        'results': results,
        'form': form
        }))