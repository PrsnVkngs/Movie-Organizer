from dataclasses import dataclass
from typing import Optional
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring
import pathlib


def remove_first_line(text):
    lines = text.split("\n")
    if len(lines) > 1:  # Make sure there are multiple lines
        return "\n".join(lines[1:])
    else:
        return ""  # Return an empty string if there is only one line or no lines


@dataclass
class MatroskaTagger:
    xml_root: Element
    tags: Element

    def __init__(self, track_uid: Optional[str] = None):
        self.xml_root = Element('Tags')
        self.tags = SubElement(self.xml_root, 'Tag')
        if track_uid is not None:
            uid_f = SubElement(self.tags, 'Targets')
            uid_v = SubElement(uid_f, 'TrackUID')
            uid_v.text = track_uid

    def add_tag(self, tag_name: str, tag_value: str):
        tag = SubElement(self.tags, 'Simple')
        name = SubElement(tag, 'Name')
        name.text = tag_name
        value = SubElement(tag, 'String')
        value.text = tag_value

    def add_subtag(self, parent_tag_name: str, tag_name: str, tag_value: str):
        for parent in self.xml_root.iter('Simple'):
            if parent.find('Name').text == parent_tag_name:
                tag = SubElement(parent, 'Simple')
                name = SubElement(tag, 'Name')
                name.text = tag_name
                value = SubElement(tag, 'String')
                value.text = tag_value

    def parse_dict(self, dictionary: dict):
        for tag, detail in dictionary.items():
            self.add_tag(str(tag).upper().strip(), str(detail).strip())

    def get_xml_string(self):
        xml_str = tostring(self.xml_root, 'utf-8')
        pretty_xml = remove_first_line(parseString(xml_str).toprettyxml(indent="  "))
        return pretty_xml

    def write_to_file(self, filename, directory):
        """
        Write the XML to a file in a given directory.

        Args:
            filename (str): The name of the file to write to.
            directory (str): The directory to write the file to.
        """
        # Combine the directory and filename to create the full path
        filepath = pathlib.Path(f'{directory}/{filename}')

        # Open the file and write the XML to it
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(remove_first_line(self.get_xml_string()))
