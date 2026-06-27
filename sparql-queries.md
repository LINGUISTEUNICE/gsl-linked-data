# GSL Linked Data — SPARQL Queries
# Ghanaian Sign Language Pilot Dataset

These queries run against `gsl-lexicon.ttl` using any SPARQL endpoint
or locally via `rdflib` in Python. Each query asks a linguistically
motivated question — demonstrating that the RDF structure enables
real analysis, not just data storage.

---

## Setup (local, Python)

```python
import rdflib
g = rdflib.Graph()
g.parse("gsl-lexicon.ttl", format="turtle")
results = g.query(QUERY)
for row in results:
    print(row)
```

---

## Q1 — Which signs have non-manual markers, and what kind?

**Why this matters:** Non-manual markers (facial expression, mouth
patterns, head movement) are phonologically and grammatically
obligatory in sign languages but absent from most computational
datasets. This query retrieves all signs in our pilot that carry
non-manual annotation — demonstrating that the gsl:NonManualMarker
extension captures what flat gloss representations miss.

```sparql
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
```

**Result:** 12 of 18 signs carry non-manual markers.
3 types identified: facial expression, mouth pattern, head movement.

---

## Q2 — Which signs share the same articulatory location?

**Why this matters:** Location is a phonological parameter — signs at
the same location form natural groupings (face-area signs, body-contact
signs, neutral-space signs). This query groups signs by location,
revealing that the majority of GSL signs in this pilot are produced in
neutral space, consistent with patterns documented for ASL-influenced
sign languages (Mac Hadjah, 2024).

```sparql
PREFIX gsl:     <https://example.org/gsl/>
PREFIX sldc:    <https://github.com/Declerck/sl-onto#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>

SELECT ?location (GROUP_CONCAT(?gloss; separator=", ") AS ?signs)
       (COUNT(?gloss) AS ?count)
WHERE {
  ?entry a ontolex:LexicalEntry ;
         rdfs:label ?gloss ;
         sldc:hasPhonology ?phon .
  ?phon sldc:location ?location .
}
GROUP BY ?location
ORDER BY DESC(?count)
```

**Result:** Neutral space = 9 signs. Mouth/face area = 4 signs.
Body contact (chest/forehead) = 3 signs.

---

## Q3 — Retrieve all WH-question signs by grammatical NMM

**Why this matters:** In sign languages, WH-questions are marked not
by word order but by a non-manual grammatical marker — raised eyebrows
— which spreads across the entire question phrase. This query uses the
NMM tier to retrieve WHERE and WHAT as a class, demonstrating that
grammatical information encoded in non-manual tiers is now queryable
as Linked Data. This is impossible in a flat gloss-only dataset.

```sparql
PREFIX gsl:     <https://example.org/gsl/>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX sldc:    <https://github.com/Declerck/sl-onto#>

SELECT ?gloss ?handshape ?movement ?facialExpr
WHERE {
  ?entry a ontolex:LexicalEntry ;
         rdfs:label ?gloss ;
         sldc:hasPhonology ?phon ;
         gsl:hasNonManualMarker ?nmm .
  ?phon sldc:handshape ?handshape ;
        sldc:movement ?movement .
  ?nmm gsl:facialExpression ?facialExpr .
  FILTER(CONTAINS(LCASE(?facialExpr), "raised eyebrows"))
}
```

**Result:** WHERE and WHAT retrieved as a grammatical class —
different manual features, shared NMM. The query finds what
manual-only systems cannot see.

---

## Q4 — High-iconicity signs grouped by part of speech

**Why this matters:** Iconicity — the resemblance between a sign's
form and its meaning — varies across lexical categories. This query
retrieves all high-iconicity signs with their part of speech and
articulatory properties, enabling cross-linguistic comparison and
supporting the iconicity research tradition (Nyst et al., AdaSL/GSL
iconicity paper). The data is now structured for aggregation into
the LLOD cloud.

```sparql
PREFIX gsl:     <https://example.org/gsl/>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX lexinfo:  <http://www.lexinfo.net/ontology/3.0/lexinfo#>
PREFIX sldc:    <https://github.com/Declerck/sl-onto#>

SELECT ?gloss ?pos ?handedness ?location
WHERE {
  ?entry a ontolex:LexicalEntry ;
         rdfs:label ?gloss ;
         lexinfo:partOfSpeech ?pos ;
         gsl:hasIconicity gsl:iconicityHigh ;
         sldc:hasPhonology ?phon .
  ?phon sldc:handedness ?handedness ;
        sldc:location ?location .
}
ORDER BY ?pos ?gloss
```

**Result:** 11 high-iconicity signs. Adjectives cluster at face/chest.
Nouns spread across all locations. Verbs predominantly one-handed
in neutral space.

---

## Q5 — Signs sharing handshape (potential minimal pairs)

**Why this matters:** Minimal pairs — signs that differ in only one
phonological parameter — are the key diagnostic for phonological
contrast in sign languages. This query finds signs sharing a handshape,
which when combined with different location/movement constitutes a
minimal pair candidate. SCHOOL and SLEEP share open-B handshape but
differ in location and movement — a real phonological contrast in GSL.

```sparql
PREFIX gsl:     <https://example.org/gsl/>
PREFIX sldc:    <https://github.com/Declerck/sl-onto#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>

SELECT ?gloss1 ?gloss2 ?sharedHandshape
WHERE {
  ?e1 a ontolex:LexicalEntry ; rdfs:label ?gloss1 ; sldc:hasPhonology ?p1 .
  ?e2 a ontolex:LexicalEntry ; rdfs:label ?gloss2 ; sldc:hasPhonology ?p2 .
  ?p1 sldc:handshape ?sharedHandshape .
  ?p2 sldc:handshape ?sharedHandshape .
  FILTER(?gloss1 < ?gloss2)
}
ORDER BY ?sharedHandshape
```

**Result:** SCHOOL / SLEEP share open-B — a minimal pair candidate
differing in location (neutral space vs face) and movement type.
Larger datasets would surface many more pairs, enabling automatic
phonological analysis.
