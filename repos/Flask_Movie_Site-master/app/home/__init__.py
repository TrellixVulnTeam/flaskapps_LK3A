#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Version  : 1.0
# @Author   : Ricky.YangRui

from flask import Blueprint

home = Blueprint("home", __name__)

import app.home.views
