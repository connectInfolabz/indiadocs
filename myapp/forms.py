from django import forms
from .models import Package


class PackageForm(forms.ModelForm):
    UNIT_CHOICES = [
        ('none', 'None'),  # Option to represent no unit selected
        ('bytes', 'Bytes'),
        ('mb', 'MB'),
        ('gb', 'GB'),
    ]

    file_size_unit = forms.ChoiceField(choices=UNIT_CHOICES)

    class Meta:
        model = Package
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        file_size = self.cleaned_data.get('file_size')
        file_size_unit = self.cleaned_data.get('file_size_unit')

        if file_size is not None and file_size_unit:
            if file_size != -1:  # Check if file_size is not -1 (no file size limit)
                if file_size_unit == 'mb':
                    file_size *= 1024 * 1024  # Convert MB to Bytes
                elif file_size_unit == 'gb':
                    file_size *= 1024 * 1024 * 1024  # Convert GB to Bytes

        # Check if file_size_unit is None or 'none' (no unit selected)
        if file_size_unit in [None, 'none']:
            # Keep file_size unchanged (preserving default behavior)
            pass

        instance.file_size = file_size

        if commit:
            instance.save()

        return instance
