# Multimodal Annotation of GSL Signs — Annotator Reflection

**Dataset:** 20 signs from the Ghanaian Sign Language Lexicon  
**Source:** Fragkiadakis, Nyst & Nyarko (2021), Zenodo. DOI: 10.5281/zenodo.4533753  
**Annotation file:** gsl-multimodal-annotation.csv  
**Annotator:** [Your name]  
**Date:** 2026  

---

## What this annotation set is

This document records the decisions, uncertainties, and limitations
encountered during multimodal annotation of 20 GSL signs from the
Fragkiadakis et al. (2021) Zenodo lexicon. Three signs (WHERE, WATER,
WORK) were annotated from direct video observation. The remaining 17
were annotated from published GSL/sign language literature and are
clearly flagged in the `annotation_source` column.

The annotation captures six dimensions per sign: handshape, location,
movement, facial expression, mouth pattern, and head movement — the
parameters corresponding to manual and non-manual tiers in ELAN-style
annotation and to the `sldc:Manual` and `gsl:NonManualMarker` classes
in the companion RDF dataset (DOI: 10.5281/zenodo.20961293).

---

## Three things I could not capture

### 1. The camera angle problem

For WATER (GSL_002), I could not confirm the thumb position in the
handshape from the available video. The citation form is a W-hand
(three fingers extended, thumb tucked), but the signer's production
showed fingers hanging loosely in a way that made the thumb invisible
or ambiguous. A single frontal camera cannot capture all articulatory
dimensions simultaneously. Multi-angle recording or depth-sensor data
would resolve this — but neither is standard in existing GSL corpora.

This is not a minor technical inconvenience. Thumb position is a
phonologically contrastive feature in sign languages. An annotation
that cannot reliably capture it has a real linguistic gap.

### 2. The mouthing question

Across all three directly observed signs — WHERE, WATER, WORK — the
signer mouths the English equivalent of the sign simultaneously with
the manual production. This is consistent and raises a genuine
analytical question: is this mouthing a phonological feature of GSL,
a contact phenomenon from the surrounding English-dominant environment,
or a signer-specific production habit?

The annotation spreadsheet has a `mouth_pattern` column, but a single
column cannot distinguish between these three possibilities. A proper
annotation scheme would need a dedicated `mouthing_type` tier with
values like `lexical_mouthing`, `mouth_gesture`, and
`contact_mouthing` — a distinction documented in sign language
linguistics (Crasborn et al., 2008) but absent from most computational
annotation schemes.

### 3. The prosodic vs grammatical NMM problem

For WORK (GSL_003), the signer produces three head nods synchronised
exactly with three hand hits. This rhythmic co-occurrence makes it
genuinely difficult to determine whether the head movement is:

- A **grammatical NMM** (marking aspect or emphasis)
- A **prosodic beat marker** (rhythmic co-articulation with the manual movement)
- A **signer-specific production habit**

The `non_manual_obligatory` column captures a binary yes/no, but this
case requires a three-way distinction the column cannot hold. This is
not a failure of annotation — it is a signal that the annotation
scheme needs more expressive power for head movement specifically.

---

## What this means for multimodal data representation

These three problems — camera angle, mouthing ambiguity, prosodic vs
grammatical NMM — are not unique to this dataset or this annotator.
They are structural limitations of current sign language data
infrastructure.

They point toward three concrete needs:

- **Multi-angle or depth-sensor video** for reliable handshape capture
- **Richer NMM taxonomies** that distinguish mouthing types and head
  movement functions
- **Tier-based annotation structures** (like ELAN) that can hold
  simultaneous, overlapping, hierarchically organised information —
  rather than flat spreadsheet columns

The companion RDF dataset (DOI: 10.5281/zenodo.20961293) attempts to
address the third point by modelling non-manual markers as structured
RDF nodes rather than flat string values. But the annotation problems
documented here show that even the RDF model is limited by the
expressiveness of what can be reliably observed and agreed upon by
annotators from single-camera video.

The gap between what sign languages express and what current data
infrastructure can capture is real, significant, and unresolved.
This annotation exercise was designed to make that gap visible from
the inside.

---

## References

Crasborn, O., Sloetjes, H., Auer, E., & Wittenburg, P. (2008).
Combining video and numeric data in the analysis of sign languages
with the ELAN annotation tool. In *Proceedings of LREC 2008*.

Fragkiadakis, M., Nyst, V., & Nyarko, M. (2021). *Ghanaian Sign
Language Lexicon*. Zenodo. https://doi.org/10.5281/zenodo.4533753

Declerck, T. (2022). Towards a new Ontology for Sign Languages.
In *Proceedings of LREC 2022* (pp. 3293–3300).
https://aclanthology.org/2022.lrec-1.423/
