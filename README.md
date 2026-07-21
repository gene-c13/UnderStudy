# UnderStudy

UnderStudy lets a tutor encode their teaching method once, so students receive
answers in that tutor's method when the tutor is unavailable.

## First answering-engine test

1. Follow [SETUP.md](SETUP.md) to configure Python and `OPENAI_API_KEY`.
2. Copy `templates/Suggested Rules Template.md` to `data/rules.md`, then have
   the tutor complete the crash course in their own words.
3. Copy `templates/build_example_template.md` to `data/build_examples/01.md`
   through `04.md`, then replace the template content with 3–4 real,
   tutor-written Q&As.
4. Compile the tutor materials into a private internal profile:

   ```bash
   python compile_rules.py
   ```

   Run this again whenever `data/rules.md` or a build example changes.
5. Run an answer:

   ```bash
   python answer.py "What is the difference between ionic and covalent bonding?"
   ```

   Or run `python answer.py` and type the question when prompted.

## Plain-GPT baseline

Use the baseline for a fair comparison: it uses the same model as UnderStudy
but has no tutor rules or teaching examples.

```bash
python baseline.py "What is the difference between ionic and covalent bonding?"
```

Or run `python baseline.py` and type the question when prompted.

## Evaluation scaffold

When the tutor releases a set of Markdown question files for evaluation, run:

```bash
python run_eval.py path/to/question_folder
```

Each `.md` file must contain one question; its filename becomes the
`question_id`. The command runs UnderStudy and the plain-GPT baseline for each
file, then writes `results/eval_output.csv`.

The score and reviewer columns are intentionally blank. The tutor should score
the answer pairs manually; before a blind review, copy the two answer columns
into a separate sheet and remove or randomize their labels. This script does
not evaluate the answers automatically.

The `data/` folder is deliberately ignored by Git because it contains the
tutor's private teaching material, including the generated internal profile.
The `templates/` folder is safe to commit.

## Lesson-recording intake

Keep only consented tutor lesson recordings in `data/recordings/`. Store the
first, unedited transcription in `data/transcripts/raw/`, then save the
tutor-reviewed version in `data/transcripts/reviewed/`. Use the reviewed
transcript to update `data/rules.md` and the build examples, then run:

```bash
python compile_rules.py
```

This refreshes `data/internal/compiled_profile.md`, which `answer.py` uses for
each UnderStudy response.
