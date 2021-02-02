import json

from sondra import document
from sondra.utils import mapjson
from sondra.api.ref import Reference
from datetime import datetime

def json_serial(bare_keys=False):
    def inner(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        elif isinstance(obj, document.Document):
            if bare_keys:
                return obj.id
            else:
                return obj.url

        raise TypeError ("Type not serializable")

    return inner


class JSON(object):
    """
    This formats the API output as JSON. Used when ;formatters=json or ;json is a parameter on the last item of a URL.

    Optional arguments:

    * **indent** (int) - Formats the JSON output for human reading by inserting newlines and indenting ``indent`` spaces.
    * **fetch** (string) - A key in the document. Fetches the sub-document(s) associated with that key.
    * **ordered** (bool) - Sorts the keys in dictionary order.
    * **bare_keys** (bool) - Sends bare foreign keys instead of URLs.
    """
    # TODO make dotted keys work in the fetch parameter.

    def __call__(self, reference, results, **kwargs):

        # handle indent the same way python's json library does
        if 'indent' in kwargs:
            kwargs['indent'] = int(kwargs['indent'])

        if 'ordered' in kwargs:
            ordered = bool(kwargs.get('ordered', False))
            del kwargs['ordered']
        else:
            ordered = False

        # fetch a foreign key reference and append it as if it were part of the document.
        if 'fetch' in kwargs:
            fetch = kwargs['fetch'].split(',')
            del kwargs['fetch']
        else:
            fetch = []

        if 'bare_keys' in kwargs:
            bare_keys = bool(kwargs.get('bare_keys', False))
            del kwargs['bare_keys']
        else:
            bare_keys = False

        print(bare_keys)

        # note this is a closure around the fetch parameter. Consider before refactoring out of the method.
        def serialize(doc):
            if isinstance(doc, document.Document):
                ret = doc.json_repr(ordered=ordered, bare_keys=bare_keys)
                for f in fetch:
                    if f in ret:
                        if isinstance(doc[f], list):
                            ret[f] = [d.json_repr(ordered=ordered, bare_keys=bare_keys) for d in doc[f]]
                        elif isinstance(doc[f], dict):
                            ret[f] = {k: v.json_repr(ordered=ordered, bare_keys=bare_keys) for k, v in doc[f].items()}
                        else:
                            ret[f] = doc[f].json_repr(ordered=ordered, bare_keys=bare_keys)
                return ret
            else:
                return doc

        result = mapjson(serialize, results)  # make sure to serialize a full Document structure if we have one.

        if not (isinstance(result, dict) or isinstance(result, list)):
            result = {"_": result}

        return 'application/json', json.dumps(result, default=json_serial(bare_keys=bare_keys), **kwargs)