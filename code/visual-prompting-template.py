import base64
import httpx
import pandas as pd
import requests
import json
import time


class AMRFredGenerator:
    def __init__(self, amr_parser='SPRING', format='TURTLE', namespace='example/', api_url='http://framester.istc.cnr.it/txt-amr-fred/api/txt-amr-fred'):
        self.amr_parser = amr_parser
        self.format = format
        self.namespace = namespace
        self.api_url = api_url
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def post_request(self, url, data, retries=5, delay=5):
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=self.headers, data=json.dumps(data))
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Attempt {attempt + 1} failed: Status {response.status_code}, Response {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}, Attempt {attempt + 1} of {retries}")
            time.sleep(delay)
        return None

    def generate_amr_fred(self, text, enhancers=None):
        data = {
            'text': text,
            'amrParser': self.amr_parser,
            'format': self.format,
            'namespace': self.namespace,
            'enhancers': enhancers if enhancers else []
        }
        response = self.post_request(self.api_url, data)
        if response is None:
            print("Failed to retrieve response from server.")
            return None
        try:
            return response.get('fredGraph')
        except (KeyError, TypeError):
            print("Error processing response data.")
            return None


class ImageProcessor:
    def __init__(self, csv_file, fewshot_urls):
        self.filename_df = pd.read_csv(csv_file)
        self.sentence_dict = dict(zip(self.filename_df.filename, self.filename_df.sentence))
        self.fewshot_data = {url: base64.b64encode(httpx.get(url).content).decode("utf-8") for url in fewshot_urls}

    def get_image_sentence(self, image_filename):
        return self.sentence_dict.get(image_filename, "No description available.")


class ConceptualBlendingTask:
    def __init__(self, client, amr_fred_generator, image_processor):
        self.client = client
        self.amr_fred_generator = amr_fred_generator
        self.image_processor = image_processor
        self.results = []

    def process_images(self, image_urls):
        for image_url in image_urls:
            image_filename = image_url.split("/")[-1]
            image_sentence = self.image_processor.get_image_sentence(image_filename)
            graph = self.amr_fred_generator.generate_amr_fred(image_sentence)
            text_prompt = f"Image filename: {image_filename}\nDescription: {image_sentence}\nGraph info: {graph}"
            print(text_prompt)

            message = self.client.chat.completions.create(
                model="some-model",
                max_tokens=1024,
                system="You are a linguist expert in metaphors and conceptual blending.",
                messages=self.create_message_payload(image_url, graph)
            )

            self.results.append({
                "filename": image_filename,
                "response": message.content
            })

        self.save_results_to_csv()

    def create_message_payload(self, image_url, graph):
        return [
            {
                "role": "user",
                "content": """Image 1: this is an image representing a metaphorical conceptual blend, see the analysis:
                Blended: STARBUCKS IS CHRISTMAS TREE
                Blendable: Starbucks coffees
                Target: Starbucks coffees
                Blendable: Christmas tree
                Source: Christmas tree
                Direction: Christmas tree → Starbucks coffee (source → target)
                Blending (key principle): Christmas"""
            },
            {
                "role": "user",
                "content": image_url
            },
            {
                "role": "user",
                "content": f"Image New: \n\n  Image base graph: {graph}\n\n Image new:"
            },
            {
                "role": "user",
                "content": """Determine, based on the example above and on the following model of conceptual blending, what conceptual blend is in Image new.
                To do that, follow these steps:
                1. Metaphors in conceptual blending have a source and target domain, which are the blendable, whose roles map. The source domain/blendable is a conceptual domain containing concepts that are typically concrete, tangible, and familiar to us. The target domain/blendable is a conceptual domain containing concepts that are typically vague and abstract. The blendable form a blended (the metaphor). Blending is the key principle overarching both blendable and blended, and the blendable roles are subsumed by the blending. Every sentence said by someone conveys an attitude that is positive, negative, or neutral. A lens is the combination of attitude and blending.
                2. Define Source (S) and Target (T) as conceptual frames containing elements ssss and tttt respectively. The Blending Function (Φ) orchestrates the creation of a Blended Space (B) by actively and dynamically mapping elements from S and T: Φ(S×T)→B. This function, Φ, not only combines elements but also integrates and transforms them, thus subsuming the original roles of ssss and tttt into new roles within B. This process reflects the overarching principle of blending where the blendable roles are absorbed and redefined by the blending roles. The Lens (Λ) further refines this process by integrating the dynamic blending with an Attitude (A).
                Using the ontology class blending:Blended, which represents the conceptual metaphor, the class blending:Blending, which is the key principle/blending function principle of blending/key frame and object properties blending:Blendable, representing source and target frames, create an RDF graph that determines what is the conceptual blending in the image new, if any. Also specify in the response the source, target, metaphor, and key frame within asterisks, such as **source: source**."""
            }
        ]

    def save_results_to_csv(self):
        df = pd.DataFrame(self.results)
        df.to_csv('images-response-senza-sentence33.csv')


# Example usage

amr_fred_generator = AMRFredGenerator()
image_processor = ImageProcessor(
    csv_file='images-response-descriptiontogiveamr2fred.csv',
    fewshot_urls=[
        "https://raw.githubusercontent.com/dersuchendee/conceptualblending/refs/heads/main/image2png.png",
        "https://raw.githubusercontent.com/dersuchendee/conceptualblending/refs/heads/main/image1png.png",
        "https://raw.githubusercontent.com/dersuchendee/conceptualblending/refs/heads/main/image3png.png"
    ]
)

conceptual_blending_task = ConceptualBlendingTask(
    client=client,  # Ensure `client` is initialized with the appropriate API client
    amr_fred_generator=amr_fred_generator,
    image_processor=image_processor
)

image_urls = ["https://raw.githubusercontent.com/dersuchendee/conceptualblending/refs/heads/main/im{}png.png".format(i) for i in range(1, 51)]
conceptual_blending_task.process_images(image_urls)
