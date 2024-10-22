import requests
import json
import pandas as pd
import csv
import re
import time
from tqdm import tqdm


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


class GraphDataExtractor:
    def __init__(self):
        pass

    @staticmethod
    def extract_graph_data(graph, target):
        data = {}
        patterns = {
            'domain': f"{target}.domain (ns\\d+:\\w+)(?:_\\d)?",
            'compared-to': f"{target}.compared-to (ns\\d+:\\w+)(?:_\\d)?",
            'attribute': f"{target}.attribute (ns\\d+:\\w+)(?:_\\d)?",
        }

        domain_pattern = f"{target}.domain ns1:neuter_1"
        if re.search(domain_pattern, graph):
            print("Domain 'ns1:neuter_1' found, skipping extraction for this target.")
            return data

        for key, pattern in patterns.items():
            match = re.search(pattern, graph)
            if match:
                data[key] = match.group(1)

        return data


class MetaphorAnalyzer:
    def __init__(self, api_key, base_url="https://api.aimlapi.com/v1"):
        self.api_key = api_key
        self.base_url = base_url

    def analyze_sentence(self, sentence, graph, sentence_text, example_graph):
        prompt = self.create_prompt(sentence, graph, sentence_text, example_graph)
        return self.send_prompt(prompt)

    def create_prompt(self, sentence, graph, sentence_text, example_graph):
        return f"You receive a text T and a frame-based knowledge graph KG that is the extraction of factual knowledge from T, following the design patterns introduced by the FRED machine reader. \n\n The KG is expressed according to: \n - the semantics of OWL2 logic language \n - frame semantics principles as formalised in the Framester schema (https://w3id.org/framester/schema/) \n - ontology design patterns (motifs) as used in the FRED machine reading tool (http://www.semantic-web-journal.net/system/files/swj1379.pdf) \n - RDF language serialized in Turtle syntax \n\n  The alignments in KG are to PropBank, WordNet, VerbAtlas, Wikidata, DBpedia, DOLCE-Zero (used prefix::dul), etc.\n Here you find the alignment to PropBank and WordNet in OWL2, which you will use jointly with Wikidata for entity linking: \n PropBank: https://www.dropbox.com/scl/fi/eemcc31s7j2ld4muyhlfj/propbank-amr-3.4.0.ttl?rlkey=do7ylojjahf1b7qblsl1v15pu&dl=0 \n WordNet: https://www.dropbox.com/scl/fi/558vohdspc4i9kyysy5at/wordnet-synset_up.ttl?rlkey=3odwjnyuejx6oxxjybnm141zt&dl=0 \n When creating individuals, use the naming policy with minuscule and indexing, e.g., a claim instance -> :claim_1 \n When creating classes, use the naming policy with camel case, e.g., a notable claim class -> :claim_1 rdf:type :NotableClaim \n When creating properties, use the naming policy with minuscule camel case, e.g., he loudly cries all day -> :male_1 :loudlyCries :time . :time :duration :day ; :frequency :always ." \
                 f"\n\n T: {sentence} \n\n" \
                 f"KG: {graph}\n\n" \
                 f"Your goal is to extend the Turtle KG with more knowledge that can be assumed from T, but it is not explicit. Using the elements of KG, add any further elements you need to extract implicit knowledge about conceptual metaphors, if there are any. If there is no conceptual metaphor, say it." \
                 f"Determine, basing on the following model of conceptual blending, if the sentence below is metaphorical or not. To do that, follow these steps: \n\n" \
                 f"1. Metaphors in conceptual blending have a source and target domain, which are the blendable, whose roles map. The source domain is a conceptual domain containing concepts that are typically concrete, tangible, and familiar to us. The target domain is a conceptual domain containing concepts that are typically vague and abstract. The blendable form a blended (the metaphor). Blending is the key principle overarching both blendable and blended, and the blendable roles are subsumed by the blending. every sentence said by someone conveys an attitude that is positive, negative, or neutral. A lens is the combination of attitude and blending." \
                 f"\n\n 2. Define Source (S) and Target (T) as conceptual frames containing elements ssss and tttt respectively. The Blending Function (Φ) orchestrates the creation of a Blended Space (B) by actively and dynamically mapping elements from S and T: Φ(S×T)→B. This function, Φ, not only combines elements but also integrates and transforms them, thus subsuming the original roles of ssss and tttt into new roles within B. This process reflects the overarching principle of blending where the blendable roles are absorbed and redefined by the blending roles. " \
                 f"\n\n 3. For example, take this sentence: 'This is what happens when science serves up facts more indigestible than evolution. We end up with a society where the masses live in outright ignorance and denial, while the dominant institutions, thanks to market and political expediency, continually reorganize themselves around actionable intelligence as it comes in.' \nAccording to blending theory, we can analyze the sentence as metaphorical because serve up and indigestible are not used in their literal meaning. Also the blending scheme is like this: with the target word: serves up. \n" \
                 f"\nAnalysis: source domain is food, target domain is facts. The two domains are different and cannot belong to the same domain." \
                 f"\nBlendable: IDEA" \
                 f"\nBlendable roles 1: cognizer, idea, idea properties" \
                 f"\nBlendable: FOOD" \
                 f"\nBlendable roles 2: food consumer, food, food properties" \
                 f"\nBlended: IDEAS ARE FOOD" \
                 f"\nBlending: Internalization" \
                 f"\nBlending roles: Internalization agent, internalization input, internalization output." \
                 f"\n Blend: IDEAS ARE FOOD" \
                 f"\nEnhanced graph: {example_graph}"
        f"Then also return the conceptual metaphor in the format <<conceptual metaphor>>. If no metaphor is evoked, return <<no metaphor>>. "

    def send_prompt(self, prompt):
        import openai
        api = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

        completion = api.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0,
            max_tokens=1000,
        )

        return completion.choices[0].message.content


class CSVProcessor:
    def __init__(self, amr_fred_generator, metaphor_analyzer, graph_extractor):
        self.amr_fred_generator = amr_fred_generator
        self.metaphor_analyzer = metaphor_analyzer
        self.graph_extractor = graph_extractor

    def process_sentences_from_csv(self, input_csv, output_csv):
        try:
            df_existing = pd.read_csv(output_csv)
            processed_sentences = set(df_existing['sentence'].unique())
        except FileNotFoundError:
            processed_sentences = set()
            df_existing = pd.DataFrame(columns=['sentence', 'metaphor', 'graph'])

        with open(input_csv, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in tqdm(reader, total=145):
                sentence = row[1]

                if sentence in processed_sentences:
                    time.sleep(2)
                    continue

                print("Processing Sentence:", sentence)
                time.sleep(5)
                fred_graph = self.amr_fred_generator.generate_amr_fred(sentence, enhancers=[])
                if fred_graph is None:
                    continue

                extracted_data = self.graph_extractor.extract_graph_data(fred_graph, 'pblr:have-degree-91')
                if extracted_data:
                    sentence_text = f"hasTargetFrame {extracted_data.get('domain', 'Unknown')}, hasSourceFrame {extracted_data.get('compared-to', 'Unknown')}, hasKeyFrame {extracted_data.get('attribute', 'Unknown')}"
                    print(sentence_text)
                else:
                    sentence_text = ""

                example_graph = '''@prefix : <http://example.org/> .
@prefix metanet: <http://www.ontologydesignpatterns.org/ont/metanet/metanetschema.ttl#> .
@prefix blending: <http://www.ontologydesignpatterns.org/ont/blending.ttl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

:FoodFrame a metanet:SourceFrame ;
    rdfs:label "Food" .

:FactsFrame a metanet:TargetFrame ;
    rdfs:label "Ideas" .

# Define the blending process
:InternalizationBlending rdf:type blending:Blending ;
    metanet:hasSourceFrame :Food ;
    metanet:hasTargetFrame :Ideas ;
    blending:hasBlendable :Ideas, :Food ;
    blending:hasBlendingRole :InternalizationAgent, :InternalizationInput, :InternalizationOutput .

:InternalizationAgent rdf:type blending:Role ;
    rdfs:label "Internalization Agent" .

:InternalizationInput rdf:type blending:Role ;
    rdfs:label "Internalization Input" .

:InternalizationOutput rdf:type blending:Role ;
    rdfs:label "Internalization Output" .

# Define the conceptual metaphor using all caps, underscore, and the form target is source
:IDEAS_ARE_FOOD rdf:type metanet:ConceptualMetaphor ;
    rdfs:label "Ideas Are Food" ;
    blending:hasBlend :IdeasAreFoodBlend .'''
                metaphorical_status = self.metaphor_analyzer.analyze_sentence(sentence, fred_graph, sentence_text, example_graph)

                df_existing = df_existing.append({
                    'sentence': sentence,
                    'metaphor': metaphorical_status,
                    'graph': fred_graph
                }, ignore_index=True)

                if len(df_existing) % 5 == 0:
                    df_existing.to_csv(output_csv, index=False)

        df_existing.to_csv(output_csv, index=False)
        print("Processing complete.")


# Example usage:

amr_fred_generator = AMRFredGenerator()
graph_extractor = GraphDataExtractor()
metaphor_analyzer = MetaphorAnalyzer(api_key="your-api-key-here")
csv_processor = CSVProcessor(amr_fred_generator, metaphor_analyzer, graph_extractor)

csv_processor.process_sentences_from_csv('df.csv', 'output.csv')
