from django import forms
from core.models import Entry

API_TOKEN = ""


def create_error_dict_from_form_errors(form_errors):
    """ formのエラーを辞書形式に変換する
        JSON形式でレスポンスに返すために利用される想定
    """
    ret = {}
    for field_name, errors in form_errors.items():
        ret[field_name] = []
        for error in errors:
            ret[field_name].append(error)
    return ret


class RegisterEntryAPIForm(forms.ModelForm):
    """ 顧客登録APIのバリデーションForm """
    token = forms.CharField()

    def clean_content(self):
        if not self.cleaned_data.get("content"):
            return
        if len(self.cleaned_data["content"]) < 20:
            raise forms.ValidationError("内容は20文字以上で入力してください")
        return self.cleaned_data["content"]

    def clean_token(self):
        if self.cleaned_data.get("token") != API_TOKEN:
            return forms.ValidationError("不正なトークンです")

    class Meta:
        model = Entry
        fields = (
            "day",
            "title",
            "content",
        )