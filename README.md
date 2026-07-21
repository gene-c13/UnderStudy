# UnderStudy

UnderStudy lets a tutor encode their teaching method once, so students receive
answers in that tutor's method when the tutor is unavailable.

## First answering-engine test

1. Follow [SETUP.md](SETUP.md) to configure Python and `OPENAI_API_KEY`.
2. Add one or more lesson transcripts to `data/transcripts/raw/`.
3. Create a tutor-reviewable draft from those transcripts:

   ```bash
   python extract_rules.py
   ```

   Review and edit `data/rules_draft.md`, then copy its approved content to
   `data/rules.md`.
4. Copy `templates/build_example_template.md` to `data/build_examples/01.md`
   through `04.md`, then replace the template content with 3–4 real,
   tutor-written Q&As.
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

The text files under `data/` are shared through Git so both teammates work
from the same transcripts, drafts, rules, examples, and evaluation materials.
Only `data/recordings/` is ignored because audio files are large; share those
through your agreed shared drive instead. The `templates/` folder is also
committed to Git.

## Lesson-recording intake

The shared `data/` folder separates automated drafts from the tutor-approved
materials used by students:

```text
data/
  recordings/incoming/              # newly uploaded, consented teacher audio
  recordings/processed/             # audio successfully transcribed
  transcripts/raw/                  # unedited transcription output
  transcripts/reviewed/             # tutor-approved transcripts
  rules_draft.md                    # AI-generated draft rules; never used directly
  extracted_examples/drafts/        # AI-suggested teaching examples
  extracted_examples/approved/      # tutor-approved candidates
  rules.md                          # final tutor-approved teaching rules
  build_examples/                   # final tutor-approved Q&A examples
```

Keep test recordings in your shared-drive recordings folder. If you later need
them locally, place copies in `data/recordings/incoming/`; Git will ignore
them. The text transcripts, drafts, rules, and examples remain shareable in
the repository.
To create a tutor-reviewable rules draft from the available transcripts, run:

```bash
python extract_rules.py
```

The script uses reviewed transcripts when any are available; otherwise it uses
the raw transcripts. It writes `data/rules_draft.md`. The tutor must review
and edit this draft before copying the approved content into `data/rules.md`.
Only `data/rules.md` and `data/build_examples/` are used for student answers.

Use [recording_manifest_template.csv](templates/recording_manifest_template.csv)
as the starting point for a private recording log. Keep the completed manifest
inside `data/`, not in `templates/`.
