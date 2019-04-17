from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s not even', params={'value':value})

def isint(value):
    if len(value)!=10:
        # raise ValidationError({
        #     'field_name_1': ["เลขโทรศัพท์ต้องมี10หลัก"],
        #     'field_name_2': ["เบอร์โทรศัพท์ต้องเป็นตัวเลข"],
        # })
        raise ValidationError("เลขโทรศัพท์ต้องมี10หลัก")
    for char in value:
        if not char.isdigit():
            raise ValidationError("เบอร์โทรศัพท์ต้องเป็นตัวเลข")

class PollForm(forms.Form):
    title = forms.CharField(label="ชื่อโพล", max_length=100,required=True)
    email = forms.CharField(validators=[validators.validate_email])
    no_questions = forms.IntegerField(label="จำนวนคำถาม", min_value=0,max_value=10,required=True,validators=[validate_even])
    start_date=forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def clean_title(self):
        data = self.cleaned_data["title"]

        if "ไอที" not in data:
            raise forms.ValidationError("name")

        return data
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and not end:
            raise forms.ValidationError("pick date")
            # self.add_error("end_date", "pick date")
        elif end and not start:
            raise forms.ValidationError("pick date")
            # self.add_error("start_date", "pick date")

class CommentForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(max_length=500,widget=forms.Textarea)
    email = forms.CharField(validators=[validators.validate_email],required=False)
    tel = forms.CharField(max_length=10,validators=[isint],required=False)


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        tel = cleaned_data.get("tel")


        if email and tel:
            raise forms.ValidationError("choose one")
        elif not email and not tel:
            raise forms.ValidationError("choose one")

class ChangePass(forms.Form):
    old_pass = forms.CharField(required=True,label="รหัสผ่านเก่า")
    new_pass = forms.CharField(min_length=8,required=True,label="รหัสผ่านใหม่")
    renew_pass = forms.CharField(min_length=8,required=True,label="ยืนยันรหัสผ่านใหม่")

    def clean(self):
        cleaned_data = super().clean()
        pa = cleaned_data.get("new_pass")
        repa = cleaned_data.get("renew_pass")


        if pa != repa:
            raise forms.ValidationError("pass must same")

class RegisterForm(forms.Form):
    GENDERS = (
        ('MALE', 'ชาย'),
        ('FEMALE', 'หญิง'),
        ('OTHER', 'อื่นๆ'),
    )

    email = forms.CharField(validators=[validators.validate_email],label="อีเมล์")
    user = forms.CharField(label="ชื่อผู้ใช้")
    newpass=forms.CharField(min_length=8,label="รหัสผ่าน")
    repass=forms.CharField(min_length=8,label="ยืนยันรหัสผ่าน")
    line_id=forms.CharField(required=False,label="LINE ID")
    facebook = forms.CharField(required=False,label="Facebook")
    gender=forms.ChoiceField(widget=forms.RadioSelect,choices=GENDERS,required=True)
    birth=forms.CharField(required=False,label="วันเกิด")

    def clean(self):
        cleaned_data = super().clean()
        pa = cleaned_data.get("newpass")
        repa = cleaned_data.get("repass")


        if pa != repa:
            raise forms.ValidationError("pass must same")