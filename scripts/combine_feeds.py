import requests
import xml.etree.ElementTree as ET
import os
import html
# Register the Google namespace once
ET.register_namespace('g', 'http://base.google.com/ns/1.0')

# Define the base URL and number of pages to fetch
base_url = "https://shop.cancerresearchuk.org/pages/xml-product-feed?page="
pages = range(1, 10)

# Create the root element for the combined RSS feed
rss = ET.Element("rss", {
    "version": "2.0",
})

channel = ET.SubElement(rss, "channel")

# Track if we have copied metadata from the first feed
metadata_copied = False

# Fetch and combine items from each page
for page in pages:
    url = f"{base_url}{page}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        # Remove duplicate xmlns:g if present
        for elem in root.iter():
            if 'xmlns:g' in elem.attrib:
                del elem.attrib['xmlns:g']

        # Extract channel and items
        page_channel = root.find("channel")
        if page_channel is not None:
            if not metadata_copied:
                # Copy metadata elements like title, link, description
                for tag in ["title", "link", "description"]:
                    element = page_channel.find(tag)
                    if element is not None:
                        channel.append(element)
                metadata_copied = True

          # Append all <item> elements with unescaped text - remove double escaped amps
            for item in page_channel.findall("item"):
                for sub in item.iter():
                    if sub.text:
                        sub.text = html.unescape(sub.text)
                    if sub.tail:
                        sub.tail = html.unescape(sub.tail)
                channel.append(item)
    except Exception as e:
        print(f"[ERROR] Page {page}: {e}")

# Ensure output directory exists
os.makedirs("docs", exist_ok=True)

# Write the combined XML to a file
tree = ET.ElementTree(rss)
tree.write("docs/combined_product_feed.xml", encoding="utf-8", xml_declaration=True)

print("✅ Combined XML product feed saved to 'docs/combined_product_feed.xml'")
