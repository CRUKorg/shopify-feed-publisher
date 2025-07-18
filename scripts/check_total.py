import xml.etree.ElementTree as ET

def count_items_in_feed(file_path="docs/combined_product_feed.xml"):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        channel = root.find("channel")
        items = channel.findall("item")
        print(f"✅ Total number of <item> elements: {len(items)}")
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error reading feed: {e}")

if __name__ == "__main__":
    count_items_in_feed()