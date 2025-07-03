# Types of Errors for Metaphor Understanding

*Overview of types of errors for metaphor understanding according to the classification in Wachowiak et al. (2023) and Petridis et al. (2019). In the evaluation, answers closely related to the gold standard are considered correct.*

## Metaphor Understanding Errors

| Task | Type of Error | Example |
|------|---------------|---------|
| **Metaphor understanding** | **Wrong with trigger** | **Sentence:** *This mini-controversy erupted when Republicans introduced a string of amendments in a final effort to obstruct passage of the reconciliation bill.* <br> **Prediction:** CONTROVERSY IS VOLCANO ERUPTION <br> **Gold Standard:** INHIBITING ENACTMENT OF LEGISLATION IS IMPEDING MOTION |
| **Metaphor understanding** | **Too literal** | **Sentence:** *[of cancer elements] Their further fate depends on various factors.* <br> **Prediction:** FATE IS DEPENDENT ON FACTORS <br> **Gold Standard:** (TUMOUR) CELLS ARE HUMAN BEINGS |
| **Metaphor understanding** | **Should be non-metaphoric** | **Sentence:** *And the black middle class has flourished in the past 20 years as opportunities in various professions have opened up.* <br> **Prediction:** SOCIOECONOMIC SYSTEM IS PLANT GROWTH <br> **Gold Standard:** Literal |
| **Metaphor understanding** | **Should be metaphoric** | **Sentence:** *Do the exercises at the end of the chapter.* <br> **Prediction:** No metaphor <br> **Gold Standard:** MIND IS A BODY |
| **Metaphor understanding** | **Too specific** | **Sentence:** *He's down with the flu* <br> **Prediction:** ILLNESS IS DOWN <br> **Gold Standard:** HEALTH IS VERTICALITY |
| **Metaphor understanding** | **Too general** | **Sentence:** *Opponents tried to dismantle the theory piece by piece.* <br> **Prediction:** THEORIES ARE PHYSICAL OBJECTS <br> **Gold Standard:** THEORIES ARE BUILDINGS |
| **Metaphor understanding** | **Wrong sub-element mapping** | **Sentence:** *Signal left turn right: central rhetoric and local reform in China.* <br> **Prediction:** POLITICAL RHETORIC IS TRAFFIC SIGNALING <br> **Gold Standard:** GOVERNMENT IS A DRIVER |

## Visual Metaphor Understanding Errors

| Task | Type of Error | Example |
|------|---------------|---------|
| **Visual metaphor understanding** | **Incorrect objects** | **Objects:** Nike shoes, lungs <br> **Prediction:** Objects: Fish, lungs <br> **Gold Standard:** Nike shoes, lungs. Property: breathe |
| **Visual metaphor understanding** | **Incorrect Property** | **Objects:** Car keys, Gun <br> **Prediction:** Property: power <br> **Gold Standard:** Property: danger |
| **Visual metaphor understanding** | **Incorrect direction of property transfer** | **Objects:** Moon, Nivea Cream <br> **Prediction:** Property: Soothing/rejuvenating <br> **Gold Standard:** Property: night |
| **Visual metaphor understanding** | **Incorrect target symbol** | **Objects:** Car Keys, Gun; Property: Dangerous <br> **Prediction:** Car keys, Gun; Property: Dangerous <br> **Gold Standard:** The LLM does not understand the car keys stand for the car, but rather addresses the fact that they can open many doors and therefore are dangerous for that. |

## References

- Wachowiak et al. (2023)
- Petridis et al. (2019)