import xml.etree.ElementTree as ET



def main():

    tree = ET.parse('osm.net.xml')

    root = tree.getroot()

    for edge in root.iter('lane'):

        if edge.get('disallow'):
            print("disallow")
            print(edge.get("speed"))

            speed = edge.get("speed")

            speed = float(speed) + 10
            edge.attrib['speed'] = str(speed)


    tree.write('osm.net.xml')

if __name__ == "__main__":

    main()