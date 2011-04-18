from haystack.indexes import RealTimeSearchIndex, CharField, MultiValueField

class ContactIndex(RealTimeSearchIndex):
    text=CharField(document=True, use_template=True)
    given_name=CharField(model_attr="given_name")
    family_name=CharField(model_attr="family_name")
    role=CharField(model_attr="role")
    organization=CharField(model_attr="organization")
    address_1=CharField(model_attr="address_line_1")
    address_2=CharField(model_attr="address_line_2")
    address_3=CharField(model_attr="address_line_3")
    note=CharField(model_attr="note", null=True)
    tag_list=MultiValueField(model_attr="tag_list", null=True)
