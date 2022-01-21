import xml.etree.ElementTree as ET
import nilearn as nl
import nilearn.image as ni
import numpy as np



def build_dict_rois(xmlfile):
    # Read XML for brain atlas
    xml_root = ET.parse(xmlfile).getroot()

    roi_names = list()
    roi_ids = list()

    for i in range(len(xml_root)):
        roi_names.append(xml_root[i].get('fullname'))
        roi_ids.append(int(xml_root[i].get('id')))

    roi_dict = {roi_ids[i]: roi_names[i]
                for i in range(len(roi_ids))}

    return roi_dict


ub_xml = build_dict_rois('/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/brainsuite_labeldescription.xml')

bt_xml = build_dict_rois('/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/Brainnetome/brainsuite_labeldescription.xml')
print(ub_xml)
print(bt_xml)

