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
import threading
import time
import urllib.request
import sys
import os
import os.path
from os import path
import shutil
import io
import json
import model_modules
from database import WriteJSONFileFS, ReadJSONFileFS
from dataset import CoreDataFrame
from user import GetAllUsers, UserSet, User
from encode import Base64, B64EncodeFile, B64DecodeFile
from hash import Hash, HashData, HashFile
from utility import Timestamp
from typing import List
from api import LibraryAPI
from enum import Enum

MODELS_LIBRARY_FILE_LOCATION: str = 'storage/models.json'
MODELS_SESSION_FILE_LOCATION: str = 'storage/model_sessions.json'
DEFAULT_MODEL_LIBRARY: str = 'storage/default_model_library.json'

'''
@name ModelComponent
@description enum type to represent the different component types
    native -
    external - for a standalone python script
'''
class ModelComponent(Enum):
    NATIVE = "native"
    EXTERNAL = "external"

'''
@name ModelDataLoader
@description
'''
class ModelDataLoader(Enum):
    LOCAL_PANDAS_CSV = "local_pandas_csv"
    LOCAL_PANDAS_PARQUET = "local_pandas_parquet"
    HDFS_PANDAS_CSV = "HDFS_pandas_csv"
    HDFS_PANDAS_PARQUET = "HDFS_pandas_parquet"
    HDFS_SPARK_CSV = "HDFS_spark_csv"
    HDFS_SPARK_PARQUET = "HDFS_spark_parquet"
    ES_GENERIC = "ES_generic"

'''
@name ModelReturnType
@description
'''
class ModelReturnType(Enum):
    USER_RISKS = "user_risks"

'''
@name Model
@description internal representation of a Model
'''
class Model():
    def __init__(self, metadata: dict, dataframe: CoreDataFrame = None):
        self.data: dict = metadata
        self.dataframe = dataframe
        # TODO dataframe should be dataframes
        # also, it should be a dict to hold many dataframes
        pass

    def run(self):
        #
        pass



'''
@name ModelEngine
@description model engine runs all deployed models
'''
class ModelEngine():
    def __init__(self):
        self.library: ModelLibrary = ModelLibrary()

        # check for model metadata storage
        try:
            '''
            import os.path
            from os import path
            path.exists()
            '''
            json_reader = ReadJSONFileFS(MODELS_LIBRARY_FILE_LOCATION)
            self.model_configuration: dict = json_reader.data
            logging.info("Model Engine:"+str(self.model_configuration.keys()))
        except Exception as e:
            logging.error("ModelEngine: ReadJSONFileFS failed: "+str(e))
            self.model_configuration: dict = ReadJSONFileFS(DEFAULT_MODEL_LIBRARY)
            WriteJSONFileFS(self.model_configuration, MODELS_LIBRARY_FILE_LOCATION)
            pass

    '''
    @name execute
    @description execute overall model job
    '''
    def execute(self):

        # TODO: reference model schedule, right now, this iterates over models sequentially
        #iterare over models groups in local model library
        for model_group_key in self.model_configuration.keys():

            # group
            model_group: dict = self.model_configuration[model_group_key]
            model_group_dataloader_context: dict = model_group["data_loader"]["data_loader_context"]
            model_group_dataloader: str = model_group["data_loader"]["data_loader_type"]
            # load data for model group to share
            if model_group_dataloader == ModelDataLoader.LOCAL_PANDAS_CSV.value:

                args: dict = {
                    'sep': ' ',
                    'header': 0,
                    'error_bad_lines': False,
                    'warn_bad_lines': False
                }

                loaded_data: CoreDataFrame = model_modules.LocalPandasCSV(model_group_dataloader_context["file_location"], model_group_dataloader_context["file"], **args).data
                print(loaded_data.data)

            elif model_group_dataloader == ModelDataLoader.LOCAL_PANDAS_PARQUET.value:
                # TODO: parquet logic\

                args: dict = {
                    'sep': ' ',
                    'header': 0,
                    'error_bad_lines': False,
                    'warn_bad_lines': False
                }

                loaded_data: CoreDataFrame = model_modules.LocalPandasParquet(model_group_dataloader_context["file_location"], **args).data
                print(loaded_data.data)

                pass

            elif model_group_dataloader == ModelDataLoader.HDFS_PANDAS_CSV.value:
                #https://creativedata.atlassian.net/wiki/spaces/SAP/pages/61177860/Python+-+Read+Write+files+from+HDFS
                # TODO: HDFS CSV logic
                args: dict = {
                    'host': 'http://localhost:6200'
                }

                loaded_data: CoreDataFrame = model_modules.HDFSPandasCSV(model_group_dataloader_context["file_location"], **args).data
                print(loaded_data.data)
                pass
            elif model_group_dataloader == ModelDataLoader.HDFS_PANDAS_PARQUET.value:
                # TODO: HDFS pandas parquet logic
                args: dict = {
                    'host': 'http://localhost:6200'
                }

                loaded_data: CoreDataFrame = model_modules.HDFSPandasParquet(model_group_dataloader_context["file_location"], **args).data
                print(loaded_data.data)
                pass

            elif model_group_dataloader == ModelDataLoader.HDFS_SPARK_CSV.value:
                # TODO: HDFS spark csv logic
                args: dict = {
                    'host': 'http://localhost:6200'
                }

                loaded_data: CoreDataFrame = model_modules.HDFSSparkCSV(model_group_dataloader_context["file_location"], **args).data
                print(loaded_data.data)
                pass
            elif model_group_dataloader == ModelDataLoader.HDFS_SPARK_PARQUET.value:
                # TODO:  HDFS spark parquet logic
                args: dict = {
                    'host': 'http://localhost:6200'
                }

                loaded_data: CoreDataFrame = model_modules.HDFSSparkParquet(model_group_dataloader_context["file_location"], **args).data
                print(loaded_data.data)
                pass

            elif model_group_dataloader == ModelDataLoader.ES_GENERIC.value:

                # TODO: elastic search query logic
                args: dict = {
                    'query': 'QUERY'
                }

                loaded_data: CoreDataFrame = model_modules.ESGeneric(model_group_dataloader_context["host"], **args).data
                print(loaded_data.data)
                pass

            else:

                unsupported_dataloader_error_message: str = "encountered unsupported data loader: "+str(model_group_key)
                logging.error(unsupported_dataloader_error_message)
                raise Exception(unsupported_dataloader_error_message)



            # iterate through model groups
            for model in model_group["models"]:
                logging.info("model engine execute model: "+str(model))
                model_metadata: dict = model
                model_enabled: bool =  model_metadata["enabled"]

                #if model is enable, load model, and run it
                if model_enabled:

                    logging.info("Model enabled: "+str(model_metadata["model_name"]))
                    model_session = ModelSession(model_metadata, self.library)

                    # TODO: new thread
                    # start model session job
                    model_result: dict = model_session.start_job(loaded_data)

                    # check if model results are empty
                    if not bool(model_result):
                        logging.warning("Model Result is empty: "+str(model_metadata["model_name"]))
                    else:
                        # model results are not empty
                        model_return_logic: dict = model_metadata["return"]
                        model_return_type: str = model_return_logic["return_type"]

                        if model_return_type == ModelReturnType.USER_RISKS.value:
                            # TODO: handle user_risks object
                            # FOR EACH user in USER_RISKS
                            # for user_from_model in model_result["users"]
                                # write user risk profile to DB
                            pass

                        pass


                else:
                    logging.warning("Model is NOT enabled: "+str(model_metadata["model_name"]))
                    pass

            # TODO: Iterate over rules?

        # end model group

'''
@name ModelLibrary
@description manage model library
'''
class ModelLibrary():
    def __init__(self):
        self.api = LibraryAPI()

    '''
    @name
    @description
    '''
    def remove_model(self, model_id: int) -> bool:
        path = "model_library/model_test"
        try:
            #os.rmdir(path)
            shutil.rmtree(path)
            print("Model removed")
            return True
        except Exception as e:
            logging.error(e)
            return False

    '''
    @name install_model
    @description install selected model from server
    '''
    def install_model(self, model: Model):

        logging.error("installing model...")

        # TODO: fetch model from API endpoint
        install_response = self.api.install(model.data["model_name"])

        logging.info("install_model() response: "+str(install_response.content.decode()))
        logging.info("install_model() raw: "+str(install_response.raw.headers))

        # Create folder
        access_rights = 0o755
        path = "model_library/"+str(model.data["model_name"])+"/"
        try:
            os.mkdir(path, access_rights)
        except Exception as e:
            logging.error(e)

        # parse model response object
        model_object: dict = json.loads(install_response.content.decode())["models"][model.data["model_name"]]

        logging.warning("install_model(), attempting to store: "+str(model.data["model_name"]))

        # TODO: store model
        self.store_model(model_object)


    '''
    @name is_installed
    @description
    '''
    def is_installed(self, model: Model):
        result: bool = True
        logging.info("is_installed: "+str( model.data["model_name"] ))
        if path.isdir("model_library/"+str(model.data["model_name"])+"/"):
            for component in model.data["components"]:
                if path.exists("model_library/"+str(model.data["model_name"])+"/"+str(component["filename"])):
                    logging.info("is_installed(): "+str( component["filename"] ))
                else:
                    logging.error("is_installed(): model component doesnt exist: "+str( component["filename"] ))
                    result = False
        else:
            logging.error("is_installed(), NO model directory: "+str( model.data["model_name"] ))
            result = False
        return result

    '''
    @name run_model
    @description invoke model execution process, and return dict (for now)
    '''
    def run_model(self, model: Model) -> dict:
        logging.warning("run_model(), attempting to run: "+str(model.data["model_name"]))

        # TODO: error handling

        # import the model
        model_path: str = 'model_library/'+str( model.data["model_name"] )


        # insert model scope
        sys.path.insert(0, model_path)
        import MODEL
        # execute model
        try:
            # TODO pass model to execution process
            # model_result: dict = MODEL.execute(model)
            model_result: dict = MODEL.execute()
        except Exception as e:
            logging.error("Model Execution Failed: "+str(model.data["model_name"])+" Reason: "+str(e))

        # remove model scope from path list
        sys.path.remove(model_path)

        # delete model scope from sys.modules
        if 'MODEL' in sys.modules:
            del sys.modules["MODEL"]

        # return standard model result
        return model_result

    '''
    @name store_model
    @description store model on disk
    '''
    def store_model(self, model: dict):

        logging.warning("storing model")
        # check if mode if installed

        #TODO verify, model_id is valid
        #TODO verify contents of model contents
        # insert at 1, 0 is the script path (or '' in REPL)
        # Iterate over components
        for component in model["components"]:
            # write binary
            f = open('model_library/'+model["model_name"] + '/' + component["filename"], 'wb')
            f.write( Base64( component["file_payload"] ).decode() )
            f.close()


'''
@name ModelDeployment
@description to alter deployed models set
'''
class ModelDeployment():
    def __init__(self, deployment_id: str):
        logging.info("Model Deployment made")
        self.did = deployment_id

'''
@Session
@description start model session. A model session can have several jobs
'''
class ModelSession():
    def __init__(self, metadata: dict, library: ModelLibrary):
        self.metadata: dict = metadata
        self.library: ModelLibrary = library

        #TODO: log model session has been initiated
        model_session_run_log_record: dict = {
            "session": metadata,
            "timestamp": Timestamp().readable
        }

        ## TODO: don't overwrite session log
        WriteJSONFileFS(model_session_run_log_record, MODELS_SESSION_FILE_LOCATION)

    '''
    @name start_job
    @description start a model session job
    @return multipurpose dict
    '''
    def start_job(self, dataframe: CoreDataFrame) -> dict:
        logging.info("Model Session: starting job")

        time.sleep(2) # TODO: remove after debug

        # create model instance
        model_instance: Model = Model(self.metadata, dataframe)

        # model library load
        logging.info(str(model_instance.data))

        # check if model is installed
        model_id: str = model_instance.data["model_name"] # could be model hash

        # pass metadata so we can verify it is installed
        # TODO: error handling
        model_result: dict = {}

        if not self.library.is_installed(model_instance):

            logging.info("Model Session, model is [NOT] installed: "+str(model_instance.data["model_name"]))
            if VerifyModel(model_instance).verify_model_encodings():

                self.library.install_model(model_instance)
                if VerifyModel(model_instance).verify_model_files():

                    #

                    model_result = self.library.run_model(model_instance)
                    logging.info("Model Session: finishing job: "+str(len(model_result)))

                else:
                    # TODO: handle error
                    logging.error("Model Failed File Verification: "+str(model_instance.data))
                    # TODO: remove model
                    #self.remove_model()
                    self.cleanup_model()
            else:
                # TODO: handle error
                logging.error("Model Failed Encoded Verification: "+str(model_instance.data))
                # TODO: remove model
                #self.remove_model()
                self.cleanup_model()

        else:
            logging.info("Model Session, model [IS] installed: "+str(model_instance.data["model_name"]))

            # only verify components installed
            if VerifyModel(model_instance).verify_model_files():

                model_result = self.library.run_model(model_instance)
                logging.info("Model Session: finishing job: "+str(len(model_result)))

                # TODO: handle model result conditioned on model_instance.data["return"] object

            else:
                # TODO: handle error
                logging.error("Model Failed File Verification: "+str(model_instance.data))
                # TODO: remove model
                #self.remove_model()
                self.cleanup_model()

        return model_result

    '''
    @name cleanup_model
    @description remove model safely, if in production mode
    @note "unsafe" mode is just to test your own models (temp solution)
          never push
    '''
    def cleanup_model(self):
        SAFE_MODE: bool = False
        if SAFE_MODE:
            self.remove_model()
        else:
            pass

'''
@name VerifyModel
@description check integrity of model
'''
MAX_COMPONENTS: int = 2
class VerifyModel():
    def __init__(self, model: Model):
        self.model: Model = model

    '''
    @name verify_model_encodings
    @description
    '''
    def verify_model_encodings(self):
        hash_check: bool = True # start as correct, if error or invalid, change to false
        try:
            model_data: dict = self.model.data
            model_components: List = model_data["components"]
            if len(model_components) > MAX_COMPONENTS:
                logging.error("MODEL HAS TOO MANY COMPONENTS: "+str( model_data["model_name"] ))
            else:
                # iterate over components
                for component in model_data["components"]:
                    model_filename: str = str(component["filename"])

                    # cryptographically profile model
                    #model_description: dict = ProfileModel(self.model, component).data()
                    #model_profile: dict = ProfileModel(model_data["model_name"]).profile()
                    model_profile: dict = ModelProfile(self.model, component).data()

                    if model_profile["data_hash"].result == component["data_hash"]:
                        logging.info("verify_model_encodings, Model is VALID: " + str( model_data["model_name"] ) )
                        logging.info("Valid Component: " + str(component["filename"]) )

                        pass # check is valid
                    else:
                        hash_check = False # check is not valid
                        pass
                    logging.warning("hash_check: "+str( hash_check ))

        except Exception as e:
            logging.error("verify_model_encodings: "+str(e))
            hash_check = False

        return hash_check



    '''
    @name verify_model_files
    @description
    '''
    def verify_model_files(self):
        hash_check: bool = True # start as correct, if error or invalid, change to false
        #try:
        model_data: dict = self.model.data
        model_components: List = model_data["components"]
        if len(model_components) > MAX_COMPONENTS:
            logging.error("MODEL HAS TOO MANY COMPONENTS: "+str( model_data["model_name"] ))
        else:
            # iterate over components
            for component in model_data["components"]:
                model_filename: str = str(component["filename"])

                # cryptographically profile model
                model_profile: dict = ModelProfile(self.model, component).files()

                if model_profile["file_hash"].result == component["file_hash"]:
                    logging.info("verify_model_files, Model is VALID: " + str( model_data["model_name"] ) )
                    logging.info("Valid Component: " + str(component["filename"]) )
                    pass # check is valid
                else:
                    hash_check = False # check is not valid
                    pass

        # except Exception as e:
        #     logging.error("verify_model_files: "+str(e))
        #     hash_check = False

        return hash_check

'''
@name ModelProfile
@description
'''
class ModelProfile():
    def __init__(self, model: Model, component: dict):
        self.model = model
        self.component = component

    def data(self):

        # hash the base 64 representation of source
        data_hash = HashData(self.component["file_payload"].encode())
        logging.warning("Computed Component data hash: "+str(data_hash.result))

        description: dict = {
            "data_hash": data_hash
        }

        return description

    def files(self):
        # hash the file
        file_hash = HashFile("model_library/"+self.model.data["model_name"]+"/"+self.component["filename"])
        logging.warning("Computed Component file hash: "+str(file_hash.result))

        description: dict = {
            "file_hash": file_hash
        }

        return description

'''
@name ProfileModel
@description return encodings and hashes for a local model
'''
class ProfileModel():
    def __init__(self, model_name: str):
        logging.info("ProfileModel: "+str(model_name))
        self.model_name: str = model_name

    def profile(self):
        raw_model_library = ReadJSONFileFS(MODELS_LIBRARY_FILE_LOCATION)
        model_library: dict = raw_model_library.data

        # iterate over model groups
        for model_group in model_library.keys():
            for model_in_group in model_library[model_group]["models"]:
                if model_in_group["model_name"] == self.model_name:
                    model: Model = Model(model_in_group)
                    description: dict = {}
                    for component in model.data["components"]:
                        description[component["filename"]+"_file_hash"] = HashFile("model_library/"+model.data["model_name"]+"/"+component["filename"]).result
                        description[component["filename"]+"_file_b64"] = B64EncodeFile("model_library/"+model.data["model_name"]+"/"+component["filename"]).result
                        description[component["filename"]+"_data_hash_b64"] = HashData(B64EncodeFile("model_library/"+model.data["model_name"]+"/"+component["filename"]).result).result
                    return description
                else:
                    pass
