from datetime import datetime
from unittest import TestCase

import pyexcel as pe
from testapp import app, db


class TestSheet:
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_single_sheet_file(self):
        array = [["id", "name"], [1, "News"], [2, "Sports"]]
        for upload_file_type in ["xls", "ods"]:
            with app.app_context():
                db.drop_all()
                db.create_all()
            print("Uploading %s" % upload_file_type)
            file_name = "test.%s" % upload_file_type
            io = pe.save_as(array=array, dest_file_type=upload_file_type)
            response = self.app.post(
                "/upload/categories",
                buffered=True,
                data={"file": (io, file_name)},
                content_type="multipart/form-data",
            )
            ret = pe.get_array(file_type="xls", file_content=response.data)
            assert array == ret


class TestBook(TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_book_file(self):
        data = {
            "category": [["id", "name"], [1, "News"], [2, "Sports"]],
            "post": [
                ["id", "title", "body", "pub_date", "category"],
                [
                    1,
                    "Title A",
                    "formal",
                    datetime(2015, 1, 20, 23, 28, 29),
                    "News",
                ],
                [
                    2,
                    "Title B",
                    "informal",
                    datetime(2015, 1, 20, 23, 28, 30),
                    "Sports",
                ],
            ],
        }
        for upload_file_type in ["xls"]:
            with app.app_context():
                db.drop_all()
                db.create_all()
            print("Uploading %s" % upload_file_type)
            file_name = "test.%s" % upload_file_type
            io = pe.save_book_as(
                bookdict=data, dest_file_type=upload_file_type
            )
            response = self.app.post(
                "/upload/all",
                buffered=True,
                data={"file": (io, file_name)},
                content_type="multipart/form-data",
            )
            ret = pe.get_book_dict(file_type="xls", file_content=response.data)
            self.assertEqual(data["category"], ret["category"])
            sheet = pe.Sheet(data["post"], name_columns_by_row=0)
            sheet.column.format("pub_date", lambda d: d.isoformat())
            sheet2 = pe.Sheet(ret["post"], name_columns_by_row=0)
            for key in sheet.colnames:
                if key == "category":
                    continue
                assert sheet.column[key] == sheet2.column[key]
            assert sheet2.column["category_id"] == [1, 2]
