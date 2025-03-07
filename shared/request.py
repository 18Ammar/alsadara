from flask import request
from shared.exceptions import InvalidRequest
def Request(required_args:set=None):
    data = {}
    if request.is_json:
        data.update(request.get_json())
    elif request.form:
        data.update(request.form.to_dict())
    else:
        data.update(request.args.to_dict())
    if required_args:
        if not required_args.issubset(data):
            missing_arg = required_args.difference(data)
            raise InvalidRequest({
                "en":"Invalid request it must include [{}] in the request".format(', '.join(missing_arg)),
                "ar":"صيغة الطلب خاطئة يجب ان يحتوي الطلب على [{}]".format(", ".join(missing_arg))
            })
    for k,v in data.items():
        if isinstance(v,str):
            if required_args and v.strip()=="" and k in required_args:
                raise InvalidRequest({
                    "en": "The value of {{{}}} should not be empty".format(k),
                    "ar": "قيمة {{{}}} لا يجب ان تكون فارغة".format(k)
                })
            data[k]=v.strip()
    return data

