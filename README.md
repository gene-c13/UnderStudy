# UnderStudy

UnderStudy lets a tutor encode their teaching method once, so students receive
answers in that tutor's method when the tutor is unavailable.

## First answering-engine test

1. Follow [SETUP.md](SETUP.md) to configure Python and `OPENAI_API_KEY`.
2. Copy `templates/tutor_rules_template.md` to `data/rules.md`, then have Hong
   Ting complete it.
3. Copy `templates/build_example_template.md` to `data/build_examples/01.md`
   through `04.md`, then replace the template content with 3–4 real,
   tutor-written Q&As.
4. Run an answer:

   ```bash
   python answer.py "What is the difference between ionic and covalent bonding?"
   ```

   Or run `python answer.py` and type the question when prompted.

The `data/` folder is deliberately ignored by Git because it contains the
tutor's private teaching material. The `templates/` folder is safe to commit.
