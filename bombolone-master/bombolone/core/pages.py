# -*- coding: utf-8 -*-
"""
core.pages.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
""" 
import re
from flask import Blueprint, g
from bson import ObjectId

# Imports inside bombolone
import bombolone.model.pages
from bombolone.core.utils import ensure_objectid
from bombolone.decorators import check_rank, get_hash
from bombolone.core.languages import Languages
from bombolone.core.validators import CheckValue

MODULE_DIR = 'modules/pages'
pages = Blueprint('pages', __name__)

check            = CheckValue()   # Check Value class
languages_object = Languages()

class Pages(object):
    """ This class allows to :
    - get_page
    - reset
    - new
    - remove
    """
    
    page         = {}
    type_label   = {}
    len_of_label = 0
    
    message      = None            # Error or succcess message
    status       = 'msg msg-error'
    
    def __init__(self, params={}, _id=None):
        """ """
        self.languages = languages_object.available_lang_code
        self.success = False
        self.params = params
        if _id is None:
            self.reset()
        else:
            self.get_page(_id)
        
    def get_page(self, _id):
        """ Get the user document from Database """
        self.page = model.pages.find(page_id=_id)
            
    def reset(self):
        """ Reset user value in Pages.page"""
        self.message      = None
        self.status       = 'msg msg-error'
        self.type_label   = {}
        self.len_of_label = 0
        self.page = { 
            "name": "",
            "from": "",
            "import": "",
            "url": {},
            "title": {},
            "description": {},
            "content": {},
            "file": "",
            "labels": []
        }
        for code in self.languages:
            self.page['url'][code] = ''
            self.page['title'][code] = ''
            self.page['description'][code] = ''
            self.page['content'][code] = []
        
    def new(self, my_rank=100):
        """ Insert new page in the database """
        if my_rank < 15:
            self.__request_first_block()
            
        self.__request_second_block()
        self.__request_content()
        self.__request_values()
        
        if self.message is None:
            model.pages.create(page=self.page)
            self.success = True
            self.status = 'msg msg-success'
            self.message = g.pages_msg('success_update_page')
        return False
        
    def update(self):
        """ Update page in the database """
        if g.my['rank'] < 15:
            self.__request_first_block()
            
        self.__request_second_block()
        self.__request_content()
        self.__request_values()
        
        if self.message is None:
            model.pages.update(page_id=self.page['_id'], page=self.page)
            self.success = True
            self.status = 'msg msg-success'
            self.message = g.pages_msg('success_update_page')
                
        return False
        
    def remove(self):
        """ Remove page from the database """        
        # It checks page _id exist and that
        # you have permission to remove that page
        if g.my['rank'] < 15:
            model.pages.remove(page_id=self.page["_id"])
        return 'nada'
        
    def __request_first_block(self):
        """ """
        form = self.params
        old_name = self.page['name']
        self.page['name'] = form['name']
        self.page['from'] = form['from']
        self.page['import'] = form['import']
        self.page['file'] = form['file']
                
        # Check that the name field is not empty
        if not len(form['name']):
            self.message = g.pages_msg('error_1')
        
        # If the name is changed
        elif old_name.lower() != self.page['name'].lower():
            try:
                new_name = str.lower(str(self.page['name']))
                regx = re.compile('^'+new_name+'$', re.IGNORECASE)
                available_name = model.pages.find(name=regx, only_one=True)
            except:
                available_name = 'Error invalid expression'
            
            # Check that the name has between 2 and 20 characters
            if not check.length(self.page['name'], 2, 20):
                self.message = g.pages_msg('error_2')
            
            # Verify that the format of the name is correct
            elif not check.username(self.page['name']):
                self.message = g.pages_msg('error_3')
            
            # Raises an error message if username is not available.
            elif not available_name is None:
                self.message = g.pages_msg('error_4')
                
        # ~
        if len(self.page['from']) and self.message is None:
            # Check that the "from" value has between 2 and 20 characters
            if not check.length(self.page['from'], 2, 20):
                self.message = g.pages_msg('error_5')
            
            # Verify that the format of the "from" value is correct
            elif not check.username(self.page['from']):
                self.message = g.pages_msg('error_6')
                             
            # Check that the "import" value has between 2 and 20 characters
            elif not check.length(self.page['import'], 2, 20):
                self.message = g.pages_msg('error_7')
            
            # Verify that the format of the "import" value is correct
            elif not check.username(self.page['import']):
                self.message = g.pages_msg('error_8')
                
        # Check that the file name field is not empty
        elif not len(self.page['file']) and self.message is None:
            self.message = g.pages_msg('error_9')
    
    def __request_second_block(self):
        """ """            
        form = self.params
        old_url = self.page['url']
        self.page['url'] = {}
        self.page['title'] = {}
        self.page['description'] = {}
        
        for i in range(10):
            key = 'url_%s' % i
            if key in self.page:
                del(self.page[key])

        self.page['url'] = form['url']
        self.page['title'] = form['title']
        self.page['description'] = form['description']
        
        # Get URL, Title and Description in any languages
        for code in self.languages:
            self.page['url'][code] = self.page['url'].get(code, '')
            self.page['title'][code] = self.page['url'].get(code, '')
            self.page['description'][code] = self.page['url'].get(code, '')

            if self.message is None:
                error_in = ' ( ' + code + ' )'
                
                # If the url is changed
                if old_url.get(code) != self.page['url'][code]:
                    url_list = self.__get_url_list(code)
                    num_urls = len(url_list)
                    
                    for code_two in self.languages:
                        field = "url_{}.{}".format(num_urls, code_two)
                        page_id = ensure_objectid(self.page["_id"]) if "_id" in self.page else None
                        available_url = model.pages.find(field=field, 
                                                         field_value=url_list, 
                                                         page_id_ne=page_id,
                                                         only_one=True)
                    print available_url
                    
                    # Check that the url is a maximum of 200 characters
                    if not check.length(self.page['url'][code], 0, 200):
                        self.message = g.pages_msg('error_b_2') + error_in
                    
                    # Verify that the format of the url is correct
                    elif len(self.page['url'][code]) and not check.url_two(self.page['url'][code]):
                        print 3, self.page['url'][code]
                        self.message = g.pages_msg('error_b_3') + error_in
                    
                    # Raises an error message if url is not available.
                    elif not available_url is None:
                        name_page = available_url['name']
                        error_where = '{0} in the "{1}" page'.format(error_in, name_page)
                        self.message = g.pages_msg('error_b_4') + error_where 
                else:
                    url_list = self.__get_url_list(code)
                    num_urls = len(url_list)
                
                if self.message is None:
                    kind_of_url = 'url_{}'.format(num_urls)
                    if not kind_of_url in self.page:
                        self.page[kind_of_url] = {}
                    self.page[kind_of_url][code] = url_list
            
    def __request_content(self):
        """ """
        form = self.params
        self.page['labels'] = form["labels"]
        self.page['content'] = form["content"]

        print self.page['content']
           
    def __request_values(self):
        """ """
        form = self.params
        
        for index, label in enumerate(self.page['content']):
            # get all the languages
            for code in self.languages:            
        
                # if label is an image
                if self.page['labels'][index]["type"] is "image":
                    name_file = upload_file(code+'_'+str(i), 'page')
                    row_label['value'] = name_file

    def __get_url_list(self, code):
        """  """
        url = self.page['url'].get(code, '')
        url_list = url.split('/')
        # Convert list with strings all to lowercase
        map(lambda x:x.lower(),url_list)
        # Save the url without slash in the end ( '/' )
        if len(url) and url[-1] == '/':
            url_list.pop()
        return url_list


def get(page_id=None):
    """ """
    if page_id is None:
        errors = [{ "message": "Page id required" }]
    elif not ensure_objectid(page_id):
        errors = [{ "message": "Bad page id" }]
    else:
        page = model.pages.find(page_id=page_id)
        if page:
            return dict(success=True, page=page)
        else:
            errors = [{ "message": "Bad page id" }]        
    return dict(success=False, errors=errors)

def get_list(sorted_by='name'):
    """Returns the pages list
    """
    page_list = model.pages.find(sorted_by='name')
    if page_list:
        return dict(success=True, page_list=page_list)
    else:
        errors = [{ "message": "Error" }]
    return dict(success=False, errors=errors)

def create(params=None, my_rank=100):
    """ """
    page_object = Pages(params=params)
    page_object.new(my_rank=my_rank)
    if page_object.success:
        data = {
            "success": True,
            "message": page_object.message,
            "page": page_object.page
        }
        return data
    errors = [{ "message": page_object.message }]
    return dict(success=False, errors=errors, page=page_object.page)

def update(params=None):
    """ """
    page = {}
    if not "_id" in params:
        errors = [{ "message": "Page id required" }]
    else:
        page_object = Pages(params=params, _id=params["_id"])
        page_object.update()
        message = page_object.message
        page = page_object.page
        if page_object.success:
            data = {
                "success": True,
                "message": message,
                "page": page
            }
            return data
        errors = [{ "message": message }]
    return dict(success=False, errors=errors, page=page)

def remove(page_id=None):
    """ """
    page_object = Pages(_id=page_id)
    success = False
    if _id:
        success = page_object.remove()
    if success:
        data = dict(success=True)
        return data
    errors = [{ "message": "error" }] 
    return dict(success=False, errors=errors)
