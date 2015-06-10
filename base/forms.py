from django import forms


class ReportForm(forms.Form):
    hashcash = forms.CharField(label='HashCash', max_length=128, required=True)
    report = forms.FileField(label='Compiled Report File', required=True)

    humanname = forms.CharField(max_length=256)
    description = forms.CharField()

    ipaddr = forms.CharField(max_length=16, required=True)
    public = forms.BooleanField(required=True)

    users_recent = forms.IntegerField()
    users_active = forms.IntegerField()
    users_total = forms.IntegerField()

    jobs_run = forms.IntegerField()
