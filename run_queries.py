"""
GSL Linked Data — run all 5 SPARQL queries against gsl-lexicon.ttl
Usage: python run_queries.py
Requires: pip install rdflib
"""

import rdflib

g = rdflib.Graph()
g.parse("gsl-lexicon.ttl", format="turtle")
print(f"Loaded {len(g)} triples from gsl-lexicon.ttl\n")

queries = {
    "Q1 — Signs with non-manual markers": """
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
ORDER BY ?gloss""",

    "Q2 — Signs grouped by location": """
PREFIX gsl:     <https://example.org/gsl/>
PREFIX sldc:    <https://github.com/Declerck/sl-onto#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
SELECT ?location (GROUP_CONCAT(?gloss; separator=", ") AS ?signs) (COUNT(?gloss) AS ?count)
WHERE {
  ?entry a ontolex:LexicalEntry ;
         rdfs:label ?gloss ;
         sldc:hasPhonology ?phon .
  ?phon sldc:location ?location .
}
GROUP BY ?location
ORDER BY DESC(?count)""",

    "Q3 — WH-question signs (raised eyebrows NMM)": """
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
}""",

    "Q4 — High-iconicity signs by part of speech": """
PREFIX gsl:     <https://example.org/gsl/>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
PREFIX lexinfo: <http://www.lexinfo.net/ontology/3.0/lexinfo#>
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
ORDER BY ?pos ?gloss""",

    "Q5 — Minimal pair candidates (shared handshape)": """
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
ORDER BY ?sharedHandshape"""
}

for name, query in queries.items():
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    results = list(g.query(query))
    if results:
        headers = [str(v) for v in g.query(query).vars]
        print("  " + " | ".join(headers))
        print("  " + "-" * 50)
        for row in results:
            vals = [str(v)[:55] if v else "—" for v in row]
            print("  " + " | ".join(vals))
    print(f"  ({len(results)} results)")
