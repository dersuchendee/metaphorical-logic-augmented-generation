# LAG Prompting Techniques for Metaphor Detection and Understanding

This repository contains the detailed prompting techniques used in the LAG (Language-enhanced graph) approach for metaphor detection and understanding, as described in our paper.

## Table of Contents
- [Core LAG Prompting Technique](#core-lag-prompting-technique)
- [Ablation Study Prompts](#ablation-study-prompts)
- [Visual Metaphor Analysis Prompts](#visual-metaphor-analysis-prompts)
- [Zero-shot and Few-shot Templates](#zero-shot-and-few-shot-templates)
- [Classification and Extraction Rules](#classification-and-extraction-rules)

## Core LAG Prompting Technique

### LAG for Metaphor Detection and Understanding

This technique involves analyzing a text T and its corresponding frame-based knowledge graph KG to detect conceptual metaphors. The KG follows OWL2 logic, Framester schema, and RDF serialized in Turtle syntax, aligned to resources like PropBank and WordNet.

**Goal:** Extend the Turtle KG with more knowledge that can be assumed from T, but it is not explicit. Using the elements of KG, and PropBank and WordNet elements as linking points, add any further elements you need to extract implicit knowledge about Conceptual metaphors, if there are any.

**Steps:**

1. Metaphors in conceptual blending have a source and target domain, which are the blendable, whose roles map. The source domain is a conceptual domain containing concepts that are typically concrete, tangible, and familiar to us. The target domain is a conceptual domain containing concepts that are typically vague and abstract.

2. Define Source (S) and Target (T) as conceptual frames containing elements *ssss* and *tttt* respectively. The Blending Function (Φ) orchestrates the creation of a Blended Space (B) by actively and dynamically mapping elements from S and T: Φ(S×T)→B.

3. **Example analysis** for the sentence: 
   > "This is what happens when science serves up facts more indigestible than evolution. We end up with a society where the masses live in outright ignorance and denial, while the dominant institutions, thanks to market and political expediency, continually reorganize themselves around actionable intelligence as it comes in."

   - **Source domain:** food
   - **Target domain:** facts
   - **Blendable:** IDEA and FOOD
   - **Blendable Roles 1:** cognizer, idea, idea properties
   - **Blendable Roles 2:** food consumer, food, food properties
   - **Blending:** Internalization
   - **Blending roles:** Internalization agent, internalization input, internalization output
   - **Blended concept:** IDEAS ARE FOOD

**Example RDF Graph:**

```turtle
@prefix : <http://example.org/> .
@prefix metanet: <http://www.ontologydesignpatterns.org/ont/metanet/metanetschema.ttl#> .
@prefix blending: <http://www.ontologydesignpatterns.org/ont/blending.ttl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

:FoodFrame a metanet:SourceFrame ;
    rdfs:label "Food" .

:FactsFrame a metanet:TargetFrame ;
    rdfs:label "Ideas" .

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

:IDEAS_ARE_FOOD rdf:type metanet:ConceptualMetaphor ;
    rdfs:label "Ideas Are Food" ;
    blending:hasBlend :IdeasAreFoodBlend .
```

**Output Format:** Return the conceptual metaphor in the format `<<conceptual metaphor>>`. If no metaphor is evoked, return `<<no metaphor>>`.

## Ablation Study Prompts

### Prompt 1: Without KG Injection

**Input:** You receive a text T.

**Text T:** {sentence}

**Instructions:** "Your goal is to extend the Turtle KG with more knowledge that can be assumed from T, but it is not explicit. Using the elements of KG, and PropBank and WordNet elements as linking points, add any further elements you need to extract implicit knowledge about Conceptual metaphors, if there are any. To do that, follow these steps:

1. Metaphors in conceptual blending have a source and target domain, which are the blendable, whose roles map. The source domain is a conceptual domain containing concepts that are typically concrete, tangible, and familiar to us. The target domain is a conceptual domain containing concepts that are typically vague and abstract.

2. Define Source (S) and Target (T) as conceptual frames containing elements *ssss* and *tttt* respectively. The Blending Function (Φ) orchestrates the creation of a Blended Space (B) by actively and dynamically mapping elements from S and T: Φ(S×T)→B.

3. Example analysis for the sentence: "This is what happens when science serves up facts more indigestible than evolution. We end up with a society where the masses live in outright ignorance and denial, while the dominant institutions, thanks to market and political expediency, continually reorganize themselves around actionable intelligence as it comes in."
   - Source domain: food, target domain: facts.
   - Blendable: IDEA and FOOD.
   - Blendable Roles 1: cognizer, idea, idea properties
   - Blendable Roles 2: food consumer, food, food properties
   - Blending: Internalization
   - Blending roles: Internalization agent, internalization input, internalization output
   - Blended concept: IDEAS ARE FOOD.

Return the conceptual metaphor in the format `<<conceptual metaphor>>`. If no metaphor is evoked, return `<<no metaphor>>`.

[Same example graph as above]

### Prompt 2: Without Conceptual Blending

**Input:** You receive a text T and a frame-based knowledge graph KG.

**Text T:** {sentence}

**KG:** {graph}

**Instructions:** Extend the Turtle KG with more knowledge that can be assumed from T, but is not explicit. Use elements of KG, and link to PropBank and WordNet for extracting implicit knowledge about conceptual metaphors.

Determine if the sentence is metaphorical. Return the conceptual metaphor in the format `<<conceptual metaphor>>`. If no metaphor is evoked, return `<<no metaphor>>`.

## Visual Metaphor Analysis Prompts

### Configuration: LAG (Full)

**Input data:** Image, sentence describing the image, base graph, conceptual blending instructions

**Template Prompt:** 
Determine, basing on the example above and on the following model of conceptual blending, what conceptual blend is in {new image}.

To do that, follow these steps:

1. Metaphors in conceptual blending have a source and target domain, which are the blendable, whose roles map. The source domain/blendable is a conceptual domain containing concepts that are typically concrete, tangible, and familiar to us. The target domain/blendable is a conceptual domain containing concepts that are typically vague and abstract. The blendable form a blended (the metaphor). Blending is the key principle overarching both blendable and blended, and the blendable roles are subsumed by the blending. Every sentence said by someone conveys an attitude that is positive, negative, or neutral. A lens is the combination of attitude and blending.

2. Define Source (S) and Target (T) as conceptual frames containing elements *ssss* and *tttt* respectively. The Blending Function (Φ) orchestrates the creation of a Blended Space (B) by actively and dynamically mapping elements from S and T: Φ(S×T)→B. Φ not only combines elements but also integrates and transforms them, thus subsuming the original roles of *ssss* and *tttt* into new roles within B. This process reflects the overarching principle of blending where the blendable roles are absorbed and redefined by the blending roles. The Lens (Λ) further refines this process by integrating the dynamic blending with an Attitude (A).

Using the ontology class blending:Blended, which represents the conceptual metaphor, the class blending:Blending, which is the key principle/blending function principle of blending/key frame and object properties blending:Blendable, representing source and target frames, create an RDF graph that determines what is the conceptual blending in the new image, if any. Also specify in the response the source, target, metaphor and key frame within asterisks, such as **source: source**.

### Few-shot Example

**Image 1:**
- Blended: EARTH IS ICE CREAM
- Blendable: Earth
- Target: Earth
- Blendable: Ice cream
- Source: Ice cream
- Direction: Ice cream → Earth (source → target)
- Blending (key principle): Melt

### Configuration: LAG without sentence

**Input data:** Image, base graph, conceptual blending instructions

**Template Prompt:** Same as the previous entry for LAG, but without the initial sentence describing the image.

### Configuration: LAG without image

**Input data:** Sentence describing the image, base graph, conceptual blending instructions

**Template Prompt:** This entry mirrors the LAG configuration but omits the image. The task focuses solely on the description and conceptual blending based on text and RDF graph information.

## Zero-shot and Few-shot Templates

### Template for BCTMD

**Analyze the sentence "{sentence}" and the examples.**

1. Begin by reading the sentence to gain a general understanding of its meaning.
2. Identify the lexical units within the sentence.
3a. Establish the contextual meaning of each unit in the sentence.
3b. Determine if any unit has a more basic, non-metaphorical meaning.
4. If a unit has both a contextual meaning and a more basic meaning that contrasts with it but aids in understanding the metaphor, mark that unit as metaphorical.
5. At this point, if it's metaphorical, determine what conceptual metaphor it evokes. Return only the conceptual metaphor in the format `<<conceptual metaphor>>`. If no metaphor is evoked, return `<<no metaphor>>`.

## Classification and Extraction Rules

### RDF Graph Extension Extraction

The extraction is performed using regular expressions (regex) to identify Turtle syntax indicators.

**Example for the sentence:** "With the official start of primary season candidates were **off** and **running** as they sought to quickly raise millions of dollars for ad buys."

```turtle
@prefix : <http://example.org/>.
@prefix metanet: <http://www.ontologydesignpatterns.org/ont/metanet/metanetschema.ttl#>.
@prefix blending: <http://www.ontologydesignpatterns.org/ont/blending.ttl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.

:RaceFrame a metanet:SourceFrame; rdfs:label "Race".
:PoliticalCampaignFrame a metanet:TargetFrame; rdfs:label "Political Campaign".
:CompetitionBlending rdf:type blending:Blending;
    metanet:hasSourceFrame :RaceFrame;
    metanet:hasTargetFrame :PoliticalCampaignFrame;
    blending:hasBlendable :Race, :PoliticalCampaign;
    blending:hasBlendingRole :Competitor, :StartingPoint, :Progress.
:Competitor rdf:type blending:Role; rdfs:label "Competitor".
:StartingPoint rdf:type blending:Role; rdfs:label "Starting Point".
:Progress rdf:type blending:Role; rdfs:label "Progress".
:POLITICAL_CAMPAIGN_IS_A_RACE rdf:type metanet:ConceptualMetaphor;
    rdfs:label "Political Campaign Is A Race";
    blending:isMetaphorical "True"^^xsd:Boolean;
    blending:hasBlend :PoliticalCampaignIsARaceBlend.
:PoliticalCampaignIsARaceBlend rdf:type blending:Blend;
    blending:hasSourceElement :off_1, :run_1;
    blending:hasTargetElement :candidate_1, :seek_1.
:candidate_1 blending:mapsTo :Competitor.
:start-01_1 blending:mapsTo :StartingPoint.
:seek_1 blending:mapsTo :Progress.
```

### Classification Process

The classification process utilizes datatype properties such as `:isMetaphorical` and the response in the dedicated format to determine the metaphorical status of sentences in the datasets. Responses are extracted using regex matching within the RDF graph, formatted to ensure clear metaphor identification.

**Example response:**
> The conceptual metaphor identified is: **POLITICAL CAMPAIGN IS A RACE**. This metaphor is evoked by the phrase "off and running," which maps the concept of starting and progressing in a race onto the domain of political campaigns. The candidates are conceptualized as runners in a race, with the start of the primary season marking the beginning of this race. The act of quickly raising funds is seen as making progress in this metaphorical race.

### Example Extraction

```
blending:isMetaphorical "True"^^xsd:Boolean;
<<POLITICAL CAMPAIGN IS A RACE>>
```

### Mapping to Labels

- If the extracted response is in all caps and in the metaphorical format, the label will be 1.
- Otherwise, when the answer is `<<no metaphor>>`, the label is 0.

### Manual Evaluation

For the BCMTD, manual checks complement the automated extraction to gain deeper understanding about source and target identification.

## Usage

These prompts can be used with large language models to:
1. Detect conceptual metaphors in text
2. Understand visual metaphors in images
3. Generate RDF knowledge graphs representing metaphorical mappings
4. Classify metaphorical vs. literal language

## Citation

If you use these prompts in your research, please cite our paper:

```bibtex
[Your citation here]
```

## License

[Your license information]
