from django import forms
from .models import Project


class ContactForms(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label="your e-mail address")
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data["message"]
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("not enough words!")
        return message


# 这是一个搜索的form
class SearchForm(forms.Form):
    pass


# 这是一个排序的form
class RangeForm(forms.Form):
    # 制作一个选择项目的下滑菜单
    choices = [("lengthAllCdr", "CDRL/H长度"),
               ("lengthCdr3", "CDR3长度"), ("history", "分析日期")]
    rangeInfo = forms.ChoiceField(choices=choices, label="排序类别")
