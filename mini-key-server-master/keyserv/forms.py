# MIT License

# Copyright(c) 2018 Samuel Hoffman

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, PasswordField, SelectField,
                     StringField, SubmitField)
from wtforms.validators import required


class LoginForm(FlaskForm):
    username = StringField("Username", [required()])
    password = PasswordField("Password", [required()])
    submit = SubmitField("Log In")


class KeyForm(FlaskForm):
    activations = IntegerField("Number of Activations",
                               default=0,
                               render_kw={"type": "number", "min": -1,
                                          "value": 0})
    application = SelectField("Application", coerce=int)

    active = BooleanField("Active", default=True)
    memo = StringField("Memo")
    hwid = StringField("Hardware Id")
    submit = SubmitField("Submit")


class AppForm(FlaskForm):
    name = StringField("Application Name")
    support = StringField("Support Message")
    submit = SubmitField("Submit")
