import base64
import httpx
import pandas as pd
import requests
import json
import re
from time import sleep


def post_request(url, data, headers, retries=5, delay=5):
    for attempt in range(retries):
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                return response.json()
            sleep(delay)
        except requests.exceptions.RequestException:
            sleep(delay)
    return None


def generate_amr_fred(text, amr_parser='SPRING', format='TURTLE', namespace='example/', enhancers=None):
    url = 'http://example.com/api'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    data = {
        'text': text, 'amrParser': amr_parser, 'format': format,
        'namespace': namespace, 'enhancers': enhancers if enhancers else []
    }
    response = post_request(url, data, headers)
    if response:
        try:
            return response.get('fredGraph')
        except KeyError:
            return None
    return None


def create_message_with_prompt(image_url, graph, example_analysis, image_data, image_media_type, fewshot_data):
    return [
        {
            "role": "user",
            "content": f"""Image 1: this is an image representing a metaphorical conceptual blend, see the analysis:
            Blended: {example_analysis['blended']}
            Blendable: {example_analysis['blendable_target']}
            Target: {example_analysis['target']}
            Blendable: {example_analysis['blendable_source']}
            Source: {example_analysis['source']}
            Direction: {example_analysis['direction']}
            Blending (key principle): {example_analysis['key_principle']}"""
        },
        {"role": "user", "content": image_url},
        {
            "role": "user",
            "content": f"Image New: \n\n  Image base graph: {graph}\n\n Image new:"
        },
        {
            "role": "user",
            "content": """Determine, based on the example above and on the following model of conceptual blending, what conceptual blend is in Image new.
            To do that, follow these steps:
            1. Metaphors in conceptual blending have a source and target domain, which are the blendable, whose roles map. 
            The source domain/blendable is a conceptual domain containing concepts that are typically concrete, tangible, and familiar to us. 
            The target domain/blendable is a conceptual domain containing concepts that are typically vague and abstract. 
            The blendable form a blended (the metaphor). Blending is the key principle overarching both blendable and blended, and the blendable roles are subsumed by the blending. 
            Every sentence said by someone conveys an attitude that is positive, negative, or neutral. A lens is the combination of attitude and blending.
            
            2. Define Source (S) and Target (T) as conceptual frames containing elements ssss and tttt respectively. 
            The Blending Function (Φ) orchestrates the creation of a Blended Space (B) by actively and dynamically mapping elements from S and T: Φ(S×T)→B. 
            This function, Φ, not only combines elements but also integrates and transforms them, thus subsuming the original roles of ssss and tttt into new roles within B. 
            This process reflects the overarching principle of blending where the blendable roles are absorbed and redefined by the blending roles. 
            The Lens (Λ) further refines this process by integrating the dynamic blending with an Attitude (A).
            
            Using the ontology class blending:Blended, which represents the conceptual metaphor, the class blending:Blending, 
            which is the key principle/blending function principle of blending/key frame and object properties blending:Blendable, representing source and target frames, 
            create an RDF graph that determines what is the conceptual blending in the image new, if any. 
            Also specify in the response the source, target, metaphor, and key frame within asterisks, such as **source: source**."""
        },
        {
            "role": "user",
            "content": {"type": "image", "source": {"type": "base64", "media_type": image_media_type, "data": image_data}}
        },
        {
            "role": "user",
            "content": {"type": "image", "source": {"type": "base64", "media_type": fewshot_data[0]['media_type'], "data": fewshot_data[0]['data']}}
        }
    ]


filename_df = pd.read_csv('input.csv')
sentence_dict = dict(zip(filename_df.filename, filename_df.sentence))

fewshot_urls = [
    "https://example.com/image1.png",
    "https://example.com/image2.png",
    "https://example.com/image3.png"
]

fewshot_data = [
    {
        "media_type": "image/png",
        "data": base64.b64encode(httpx.get(url).content).decode("utf-8")
    }
    for url in fewshot_urls
]

base_url = "https://example.com/im{}png.png"
image_urls = [base_url.format(i) for i in range(1, 51)]

example_analysis = {
    "blended": "STARBUCKS IS CHRISTMAS TREE",
    "blendable_target": "Starbucks coffees",
    "target": "Starbucks coffees",
    "blendable_source": "Christmas tree",
    "source": "Christmas tree",
    "direction": "Christmas tree → Starbucks coffee (source → target)",
    "key_principle": "Christmas"
}

results = []
for image_url in image_urls:
    image_filename = image_url.split("/")[-1]
    image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
    image_media_type = "image/png"
    image_sentence = sentence_dict.get(image_filename, "No description available.")
    graph = generate_amr_fred(image_sentence)
    message = create_message_with_prompt(image_url, graph, example_analysis, image_data, image_media_type, fewshot_data)
    results.append({"filename": image_filename, "response": message})

df = pd.DataFrame(results)
df.to_csv('output.csv', index=False)
