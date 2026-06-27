# GSL Linked Data — Ghanaian Sign Language as Linked Open Data (Pilot)

A pilot project representing 18 signs from **Ghanaian Sign Language (GSL)**
as RDF Linked Data, using [OntoLex-Lemon](https://www.w3.org/community/ontolex/)
and the [Declerck (2022) sign language ontology](https://aclanthology.org/2022.lrec-1.423/)
(`sldc`). The first Linked Data treatment of GSL vocabulary.

---

## The problem this addresses

Sign languages are systematically absent from the
[Linguistic Linked Open Data (LLOD) cloud](https://linguistic-lod.org/).
Existing sign language datasets fall into two silos:

- **Corpus/annotation tools** (ELAN/EAF) — rich multimodal annotation,
  but locked in proprietary XML, not queryable as Linked Data
- **Computer vision datasets** — OpenPose skeletal data, useful for ML,
  but without linguistic structure

Neither silo is interoperable with the broader LLOD ecosystem. This project
demonstrates how a sign language lexicon can be modelled in RDF, making
phonological and grammatical features — including **non-manual markers**
(facial expression, mouth patterns, head movement) — queryable via SPARQL.

GSL is chosen deliberately: it is an under-resourced African sign language
with no prior Linked Data representation, making even a small pilot a
genuine contribution to the field.

---

## What is in this repository

```
gsl-linked-data/
├── README.md               ← this file
├── gsl-lexicon.ttl         ← 18 GSL signs as RDF/Turtle (353 triples)
├── sparql-queries.md       ← 5 linguistically motivated SPARQL queries
│                             with results and linguistic commentary
└── LICENSE                 ← CC BY 4.0
```

---

## Data sources

| Signs | Source | License |
|---|---|---|
| 16 signs | Fragkiadakis, Nyst & Nyarko (2021). *Ghanaian Sign Language Lexicon*. Zenodo. [DOI: 10.5281/zenodo.4533753](https://doi.org/10.5281/zenodo.4533753) | CC BY 4.0 |
| 2 signs (FATHER, HAPPY) | Author's own GSL knowledge, cross-referenced against the Ghana National Association of the Deaf (GNAD) dictionary | — |

---

## Ontologies and vocabularies used

| Prefix | Namespace | Role |
|---|---|---|
| `ontolex` | http://www.w3.org/ns/lemon/ontolex# | Lexical entry / form structure |
| `lexinfo` | http://www.lexinfo.net/ontology/3.0/lexinfo# | Part of speech |
| `sldc` | https://github.com/Declerck/sl-onto# | Sign-specific phonological features |
| `gsl` | https://example.org/gsl/ | GSL-specific extensions (non-manual markers, iconicity) |
| `prov` | http://www.w3.org/ns/prov# | Data provenance |
| `dct` | http://purl.org/dc/terms/ | Dataset metadata |

---

## The RDF model

Each sign is modelled as an `ontolex:LexicalEntry` with two feature nodes:

```
gsl:entry_THANKYOU
    a ontolex:LexicalEntry
    ├── ontolex:canonicalForm → gsl:form_THANKYOU (writtenRep "THANK-YOU")
    ├── lexinfo:partOfSpeech  → lexinfo:interjection
    ├── sldc:hasPhonology     → gsl:phon_THANKYOU   [sldc:Manual]
    │     ├── sldc:handshape    "open-B / flat hand"
    │     ├── sldc:location     "mouth / chin area"
    │     ├── sldc:orientation  "palm toward face"
    │     ├── sldc:movement     "single outward path arc"
    │     └── sldc:handedness   "one-handed"
    ├── gsl:hasNonManualMarker → gsl:nmm_THANKYOU   [gsl:NonManualMarker]
    │     ├── gsl:facialExpression  "smile, gratitude expression"
    │     └── gsl:mouthPattern      "lips slightly open"
    ├── gsl:hasIconicity      → gsl:iconicityHigh
    └── prov:wasDerivedFrom   → gsl:sourceZenodo
```

### The key extension: non-manual markers as RDF

Declerck (2022) identifies non-manual features as an open modelling
problem. This project proposes a `gsl:NonManualMarker` class with three
subclasses — `gsl:FacialExpression`, `gsl:MouthPattern`,
`gsl:HeadMovement` — attached to each sign entry. This makes non-manual
phonological and grammatical features queryable for the first time in
a GSL dataset.

---

## SPARQL queries

Five queries are documented in [`sparql-queries.md`](sparql-queries.md).
The most significant result:

**Q3 — Retrieving WH-question signs by grammatical NMM:**

WHERE and WHAT have different manual features (different handshape,
different movement) but are retrieved as a grammatical class because
they share a non-manual marker (raised eyebrows). This is impossible
in a gloss-only dataset. The RDF model finds it in one query.

### Run locally (Python + rdflib)

```bash
pip install rdflib
```

```python
import rdflib

g = rdflib.Graph()
g.parse("gsl-lexicon.ttl", format="turtle")

query = """
PREFIX gsl:     <https://example.org/gsl/>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>

SELECT ?gloss ?facialExpr ?mouthPattern ?headMovement
WHERE {
  ?entry a ontolex:LexicalEntry ;
         rdfs:label ?gloss ;
         gsl:hasNonManualMarker ?nmm .
  OPTIONAL { ?nmm gsl:facialExpression ?facialExpr }
  OPTIONAL { ?nmm gsl:mouthPattern ?mouthPattern }
  OPTIONAL { ?nmm gsl:headMovement ?headMovement }
}
ORDER BY ?gloss
"""

for row in g.query(query):
    print(row)
```

---

## Linguistic coverage of the 18 signs

| Dimension | Coverage |
|---|---|
| Handedness | 8 one-handed, 10 two-handed |
| Location | Neutral space (9), mouth/face (5), chest/body (4) |
| Non-manual markers | 12 of 18 signs carry NMMs |
| NMM types | Facial expression, mouth pattern, head movement |
| Iconicity | High (11), medium (4), low (3) |
| Semantic categories | Nouns, verbs, adjectives, question words, negation, proper noun, social/pragmatic |
| Data sources | 16 Zenodo corpus, 2 annotator knowledge |

---

## Limitations and future work

This is a deliberately small pilot. Known limitations:

1. **Scale** — 18 signs from a 1,199-sign lexicon. The model is designed
   to scale; the next step is converting the full Zenodo lexicon.
2. **Location values are string literals** — a production version would
   mint named individuals (`gsl:locationMouthChin`) for proper SPARQL
   filtering and cross-dataset linking.
3. **No video/pose linkage** — the Zenodo dataset includes OpenPose
   skeletal data per sign. Linking RDF annotation nodes to pose data
   URIs is an open modelling problem and a natural next step.
4. **Annotation uncertainty** — two signs (FATHER, HAPPY) are annotated
   from author knowledge rather than the corpus video. These are flagged
   via `prov:wasDerivedFrom gsl:sourceOwnKnowledge`.

---

## Citation

If you use this dataset or build on it, please cite:

```
[Your Name] (2026). GSL Linked Data: Ghanaian Sign Language as
Linked Open Data (Pilot). GitHub.
https://github.com/[your-username]/gsl-linked-data

Fragkiadakis, M., Nyst, V., & Nyarko, M. (2021). Ghanaian Sign
Language Lexicon. Zenodo. https://doi.org/10.5281/zenodo.4533753

Declerck, T. (2022). Towards a new Ontology for Sign Languages.
In Proceedings of LREC 2022 (pp. 3293–3300).
https://aclanthology.org/2022.lrec-1.423/
```

---

## License

This dataset is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
matching the license of the source data (Fragkiadakis et al., 2021).

---

## Contact

[Eunice Esi Essuman] — [essumaneeunice@gmail.com]
