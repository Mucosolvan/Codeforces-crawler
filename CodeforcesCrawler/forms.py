from django import forms

class TagForm(forms.Form):
    def __init__(self, connection, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        for i in connection.smembers("tags"):
            print (i.decode('utf-8'))
        self.fields['tags'] = forms.ChoiceField(
            choices=[(i, i) for i in connection.smembers("tags")]
        )

class DifficultyForm(forms.Form):
    def __init__(self, connection, *args, **kwargs):
        super(DifficultyForm, self).__init__(*args, **kwargs)
        self.fields['difficulty'] = forms.ChoiceField(
            choices=[(i, i) for i in connection.smembers("difficulties")]
        )