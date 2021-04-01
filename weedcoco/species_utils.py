import zipfile
from collections import defaultdict
import requests
from xml.etree import ElementTree


class EppoTaxonomy:
    def __init__(self, path=None, languages=("en",), types=("SPT", "PFL")):
        taxonomy = self._parse_xml(path)
        self.entries = self._extract_entries(taxonomy, languages=languages, types=types)
        children = self._extract_children(self.entries)
        for parent, children in children.items():
            self.entries[parent]["children"] = children

        self._by_preferred_name = {
            entry["preferred_name"]: entry for entry in self.entries.values()
        }
        self._by_lang_name = defaultdict(list)
        for entry in self.entries.values():
            for lang in languages:
                for name in entry.get(lang + "_names", ()):
                    self._by_lang_name[lang, name].append(entry)
        self._by_lang_name.default_factory = None

    @staticmethod
    def _parse_xml(path):
        if path is None:
            path = requests.get("https://data.eppo.int/files/xmlfull.zip").content
        if hasattr(path, "endswith") and path.endswith(".xml"):
            file = open(path)
        else:
            file = zipfile.ZipFile(path).open("fullcodes.xml")

        with file:
            root = ElementTree.parse(file)
        return root

    @staticmethod
    def _extract_entries(taxonomy, languages, types):
        entries = {}

        elems = []
        for typ in types:
            elems.extend(taxonomy.findall(f"./code[@isactive='true'][@type='{typ}']"))

        for code_elem in elems:
            code = code_elem.find("./eppocode").text
            parent_code = getattr(
                code_elem.find(".//parent[@linktype='taxo']"), "text", None
            )
            preferred_name_elem = code_elem.find(
                ".//name[@ispreferred='true'][@isactive='true']//fullname"
            )

            name_elems = code_elem.findall(
                ".//name"
            )  # XXX: can't get xpath filter on [//lang/*[text() = "en"]] working
            if preferred_name_elem is None:
                preferred_name = f"EPPO:{code} [no preferred name]"
            else:
                preferred_name = preferred_name_elem.text

            entry = {
                "code": code,
                "parent_code": parent_code,
                "level": "species" if code_elem.attrib["type"] == "PFL" else "group",
                "preferred_name": preferred_name,
            }
            for lang in languages:
                entry[lang + "_names"] = [
                    elem.find("./fullname").text
                    for elem in name_elems
                    if elem.find("./lang").text == lang and elem.find("./fullname").text
                ]
            entries[code] = entry

        return entries

    @staticmethod
    def _extract_children(entries):
        children = defaultdict(set)
        for entry in entries.values():
            children[entry["parent_code"]].add(entry["code"])
        children.default_factory = None
        return children

    def _set_ancestry(self, code, ancestry):
        entry = self.entries[code]
        entry["ancestry"] = ancestry
        path = [code] + ancestry
        for child_code in self.children[code]:
            self._set_ancestry(child_code, path)

    def lookup_preferred_name(self, name, species_only=False):
        out = self._by_preferred_name[name]
        if species_only and out["level"] != "species":
            raise KeyError(f"{name} is not a species")
        return out

    def lookup_unique_name(self, lang, name, species_only=False):
        out = self._by_lang_name[lang, name]
        if len(out) != 1:
            raise KeyError(f"{name} is not unique")
        out = out[0]
        if species_only and out["level"] != "species":
            raise KeyError(f"{name} is not a species")
        return out


# in utils.py?
def get_eppo_singleton():
    pass
