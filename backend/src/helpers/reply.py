from google.protobuf.message import Message


def reply_to_dict(reply: Message):
    result = {}
    for field in reply.DESCRIPTOR.fields:
        attr_name = field.name
        result[attr_name] = getattr(reply, attr_name)
    return result