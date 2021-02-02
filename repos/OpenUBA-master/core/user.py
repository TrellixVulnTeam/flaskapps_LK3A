'''
Copyright 2019-Present The OpenUBA Platform Authors
This file is part of the OpenUBA Platform library.
The OpenUBA Platform is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
The OpenUBA Platform is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License
along with the OpenUBA Platform. If not, see <http://www.gnu.org/licenses/>.
'''

import logging
from database import DBReadFile, DBWriteFile, WriteNewActorToDB, ReadActorFromDB, WriteJSONFileFS, ReadJSONFileFS, WriteListToDirectories
from dataset import Dataset, DatasetSession, CoreDataFrame
from typing import Dict, Tuple, Sequence, List
import pandas as pd
from pandas import DataFrame
import numpy as np

USERS_FILE_LOCATION = 'storage/users.json'
'''
@name User
@description fundamental description of
'''
class User:
    def __init__(self, user_id):
        logging.info("user initiated: "+str(user_id))
        self.user_id = user_id


'''
@name UserSet
@description wrapper to hold a set of users
'''
class UserSet():
    def __init__(self, users_dict: dict):
        self.users: dict = users_dict


'''
@name WriteUserSet
@description write a json object to a file

import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
'''
class WriteUserSet(DBWriteFile):
    @staticmethod
    def write(new_user_set: UserSet):
        # TODO: don't overwrite user set each time, just insert new keys
        current_user_set: UserSet = ReadUserSet.read()

        # iteratively add user to UserSet
        for user in new_user_set.users.keys():
            # TODO: check if user exists
            logging.error(user)
            current_user_set.users[user] = {}

        #data: dict = {"users": [u.user_id for u in new_user_set.users]}
        # no list compresension since its a dict
        data: dict = {"users": current_user_set.users}
        users_file_location: str = USERS_FILE_LOCATION

        # write JSON object for user set
        WriteJSONFileFS(data, users_file_location)

        #TODO: write users to unique directory
        try:
            user_list: List = list( data["users"].keys() )
            try:
                WriteListToDirectories(user_list, "storage/users")
            except Exception as e:
                logging.error(''.join( [str(e), str(" -- ")] ))
                raise e
        except Exception as e:
            logging.error(''.join( [str(e), str(" -- could not convert data['users'].keys() ")] ))



'''
@name ReadUserSet
@description Read a json object to a file
'''
class ReadUserSet(DBReadFile):
    @staticmethod
    def read() -> UserSet:
        users_file_location: str = USERS_FILE_LOCATION
        user_dict: dict = ReadJSONFileFS(users_file_location).data
        #return UserSet( list(user_dict.keys()) )
        return UserSet( user_dict["users"] )


'''
@name GetAllUser
@description fetch all users from the actual DB
'''
class GetAllUsers(DBReadFile):
    def get(self) -> dict:
        logging.info("read_user")
        #TODO: fetch all users from storage, should not compute all users (inefficient)
        #users = self.read_file()
        return {"user1": {}, "user2": {}}


'''
@name StoreUserRisks
@description fetch all users from the actual DB
'''

class ExtractAllUsersCSV(DBReadFile):
    '''
    @name get
    @description invoke extract all users from csv file
    '''
    @staticmethod
    def get(log_dataset_session: DatasetSession, log_metadata_obj: dict) -> UserSet:
        logging.info("extracting all users")
        extracted_users: List = ExtractAllUsersCSV.extract_users(log_dataset_session, log_metadata_obj)

        # convert list to
        user_set: UserSet = ExtractAllUsersCSV.from_raw_list(extracted_users)

        # TODO: write extracted users
        WriteUserSet.write(user_set)
        return user_set

    '''
    @name extract_users
    @description return set of unique elements from a dataset session,
                 using a configured id-feature
    '''
    @staticmethod
    def extract_users(dataset_session: DatasetSession, log_metadata_obj: dict) -> List:
        ############## TESTS
        # get dataset
        log_file_dataset: Dataset = dataset_session.get_csv_dataset()
        # get core dataframe
        log_file_core_dataframe: CoreDataFrame = log_file_dataset.get_dataframe()
        # get data frame (.data)
        log_file_dataframe: pd.DataFrame = log_file_core_dataframe.data
        # test: get shape
        log_file_shape: Tuple = log_file_dataframe.shape
        logging.warning("execute(): dataframe shape: "+str(log_file_shape))
        ############

        logging.info("ExtractAllUsersCSV: extract_users log_file_data.columns: - "+str(log_file_dataframe.columns))
        logging.info("ExtractAllUsersCSV: extract_users log_metadata_obj: - "+str(log_metadata_obj))


        id_column: pd.Series = log_file_dataframe[ log_metadata_obj["id_feature"]]
        logging.info( "ExtractAllUsersCSV, extract_users, id_column, len of column: "+str(len(id_column)) )
        user_set: List = np.unique( log_file_dataframe[ log_metadata_obj["id_feature"] ].fillna("NA") )
        logging.info( "ExtractAllUsersCSV, extract_users, user_set len of column: "+str(len(user_set)) )
        logging.error(user_set)
        return user_set


    '''
    @name from_raw_list
    @description accept a list of users, and return an actual UserSet
    '''
    @staticmethod
    def from_raw_list(user_set: List) -> UserSet:
        # iterate over user_set list
        #set_of_users: List = [User(u) for u in user_set]
        user_dict: dict = {}
        for u in user_set:
            user_dict[u] = {}
        #return UserSet(set_of_users)
        return UserSet(user_dict)
