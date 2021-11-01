from flask import Flask, send_from_directory
import xml.etree.ElementTree as ET

app = Flask(__name__, static_url_path='')


def generate_search():
    global short_name
    short_name = input("ShortName: ")
    decription = input("Description: ")
    image = input("Image: ")
    url = input("Url: ")
    param = input("Search Param: ")

    root_element = ET.Element("OpenSearchDescription", attrib={"xmlns": "http://a9.com/-/spec/opensearch/1.1/", "xmlns:moz": "http://www.mozilla.org/2006/browser/search/"})

    name_element = ET.SubElement(root_element, "ShortName")
    name_element.text = short_name

    description_element = ET.SubElement(root_element, "Description")
    description_element.text = decription

    image_element = ET.SubElement(root_element, "Image", attrib={"height": "16", "width": "16", "type": "image/x-icon"})
    image_element.text = image

    url_element = ET.SubElement(root_element, "Url", attrib={"type": "text/html", "template": url})
    _ = ET.SubElement(url_element, "Param", attrib={"name": f"{param}", "value": "{searchTerms}"})

    encoding_element = ET.SubElement(root_element, "InputEncoding")
    encoding_element.text = "UTF-8"

    element_tree = ET.ElementTree(root_element)

    ET.indent(element_tree)
    ET.dump(element_tree)
    element_tree.write(f"output/{short_name}.xml")


@app.route("/")
def host():
    return f"""
    <html>
      <link rel="search"
        type="application/opensearchdescription+xml"
        title="{short_name}"
        href="files/{short_name}.xml">
    </html>
    """


@app.route("/files/<path:name>")
def serve_files(name):
    return send_from_directory('output/', name)


if __name__ == "__main__":
    generate_search()
    app.run()
