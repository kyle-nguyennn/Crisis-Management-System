from django.conf import settings
import requests
import xml.etree.ElementTree as ET


def get_psi_reading():
    url = "http://api.nea.gov.sg/api/WebAPI/?dataset=psi_update&keyref=" + settings.NEA_KEY
    r = requests.get(url)
    root = ET.fromstring(r.text)
    NPSI_node_list = root.findall("./item/region/record/reading[1]")
    region_node_list = root.findall("./item/region/id")

    NPSI_value_list = [i.get('value') for i in NPSI_node_list]
    region_value_list = [j.text for j in region_node_list]

    result = dict(zip(region_value_list, NPSI_value_list))

    return result


def get_north_psi_reading():
    reading_dict = get_psi_reading()
    return reading_dict['rNO']


def get_south_psi_reading():
    reading_dict = get_psi_reading()
    return reading_dict['rSO']


def get_central_psi_reading():
    reading_dict = get_psi_reading()
    return reading_dict['rCE']


def get_west_psi_reading():
    reading_dict = get_psi_reading()
    return reading_dict['rWE']


def get_east_psi_reading():
    reading_dict = get_psi_reading()
    return reading_dict['rEA']
