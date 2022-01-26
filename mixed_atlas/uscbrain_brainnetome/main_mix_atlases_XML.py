import xml.etree.ElementTree as ET
import nilearn as nl
import nilearn.image as ni
import numpy as np
import copy


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


out_xml = copy.deepcopy(ub_xml)

brainnnetome_ids = [163, 164, 165, 166,
                     167, 168, 169, 170, 171, 172, 173, 174]
uscbrain_new_ids = [563, 564, 565, 566,
                     567, 568, 569, 570, 571, 572, 573, 574]


xml_root = ET.parse('/ImagePTE1/ajoshi/code_farm/svreg/USCBrainMulti/brainsuite_labeldescription.xml').getroot()

    for i in range(len(xml_root)):
        roi_names.append(xml_root[i].get('fullname'))
        roi_ids.append(int(xml_root[i].get('id')))



for ind, uid in enumerate(uscbrain_new_ids):
    print(ub_xml[uid],)
