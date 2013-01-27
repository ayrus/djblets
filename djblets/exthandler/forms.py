from django import forms


class AddExtensionForm(forms.Form):
	"""
	Form for adding extensions on the extenion manager interface.
	"""
    extension_URL = forms.URLField(label="Extension URL", required=True)

    package_name = forms.CharField(label="Package Name", required=True)
