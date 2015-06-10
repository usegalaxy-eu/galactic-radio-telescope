from django import forms


class ReportForm(forms.Form):
    hashcash = forms.CharField(label='HashCash', max_length=128, required=True)
    report = forms.FileField(label='Compiled Report File', required=True)
