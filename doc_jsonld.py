import json

def generate_json_ld(lista):
    entries = lista.split('\n')
    doc_nodes = []
    for entry in entries:
        if '#' in entry:
            name = entry.split('#')[1]
            doc_link = entry.split('\n')[0]
            short_desc = entry.split('#')[0]
            doc_node = {
                "@type": "EntryPoint",
                "@id": f"#tweepy.{name}",
                "name": name,
                "description": short_desc,
                "url": doc_link
            }
            doc_nodes.append(doc_node)

    json_ld = {
        "@context": "https://schema.org/",
        "@type": "SoftwareApplication",
        "name": "Tweepy",
        "description": "Tweepy is an easy-to-use Python library for accessing the Twitter API.",
        "url": "https://github.com/tweepy/tweepy",
        "documentation": {
            "@type": "ItemList",
            "name": "Tweepy API documentation",
            "description": "List of Tweepy client methods with links to the Twitter API documentation.",
            "itemListElement": doc_nodes
        }
    }
    
    graph = {"@graph": [json_ld]}
    
    return graph

def daj_link(soup):
    links = soup.find_all("a")
    for link in links:
        print(link.get("href"))