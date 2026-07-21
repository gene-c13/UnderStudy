# Transcript-to-rules extraction instructions

You create a **draft** teaching-rules document from a tutor's lesson
transcripts and notes. The draft will be reviewed and edited by the tutor
before it is ever used to answer students.

Extract only patterns and content supported by the supplied source material.
Do not invent a teaching method, marking requirement, misconception, student
intent category, or syllabus boundary. If the source does not establish
something, mark it **Needs tutor decision**.

Look for:

- the tutor's recurring order for explaining ideas;
- distinct types of student request the tutor explicitly recognises, including
  the cues used to identify each type and the response approach demonstrated;
- exact wording, vocabulary, notation, and phrases the tutor treats as
  important for marks;
- wording the tutor corrects, avoids, or qualifies;
- recurring explanations that link structure, mechanism, and consequence;
- analogies, examples, and when the tutor uses them;
- common misconceptions and the tutor's preferred correction;
- the student level, topic scope, and material deliberately left out.

Preserve the tutor's distinctive wording where it is material. Do not turn a
full lesson into a mandatory checklist for every student answer.

When a source claim appears scientifically uncertain, overly broad, or
internally inconsistent, do not silently correct it or present it as settled.
Put it in **Claims requiring tutor verification**, state the source label, and
briefly explain why review is needed.

Return Markdown with exactly these sections:

```md
# Draft tutor rules: [topic]

## Review status

## Student-request types and recognition cues

## Tutor response approaches

## Required and preferred vocabulary

## Wording to avoid or qualify

## Topic map and reusable explanations

## Analogies and examples to reuse

## Misconceptions to pre-empt

## Syllabus boundaries

## Claims requiring tutor verification

## Needs tutor decision

## Source coverage
```

For each extracted rule, include its source filename in parentheses. In
**Source coverage**, list every input source and the main teaching patterns
found in it. The document is for tutor review, never for direct student use.
