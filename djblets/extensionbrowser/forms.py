from django import forms
from django.utils.translation import ugettext as _


class AddExtensionForm(forms.Form):
    """Form for adding extensions.

    This form handles installing new extensions from a remote URL,
    through the extension browser interface.
    """
    extension_url = forms.URLField(label=_("Extension URL"), required=True)
    package_name = forms.CharField(label=_("Package Name"), required=True)
