

 Which tools I used

 **Claude ** the only AI tool I used for this lab.
 No other assistant (ChatGPT, Gemini, Copilot) was used.

 What I used it for

1. **Environment.** I ran the notebook locally instead of Colab, so I used Claude to set up a virtual
   environment with torch (CPU build), transformers and matplotlib, and to execute the notebook
   from the command line. This part is setup only it does not change any result of the lab.
2. **Wording of the written answers.** I wrote my predictions and my conclusions first, and then used
   Claude to help me phrase them in clearer English and to check that my explanation of *why* something
   happens (byte-level BPE, the order-preserving property of temperature, the attention sink) matches
   what the lecture actually said. Where Claude suggested a formulation I kept it only if I could
   explain it myself.
3. **Checking my reasoning.** I asked it to challenge two of my answers: whether temperature can ever
   change the #1 token, and whether "Kazakh is worse than Russian" follows from one sentence pair. Both
   checks changed what I wrote — the second one made me separate tokens-per-character (1.10 vs 1.11,
   basically equal) from total tokens (34 vs 31).

 What I did without AI

- All four predictions were written down before running the corresponding cell, as the lab requires.
- Every number quoted in my answers comes from my own run of the notebook, not from the model: the
  19 tokens for `бөлімшеңізде`, 22.87% for ` Ast` against 22.08% for ` Paris`, the temperature and
  entropy table, layer 4 head 11 for the previous-token pattern, layer 7 head 10 for the token-0 head,
  and the Part 3 token counts.
- Choosing the three prompts in `MY_PROMPTS` and reading the two heat maps was my own work.

 Verification

I compared my results with the reference values published in the lab README (extension task 2 and 3).
They agree: the previous-token head is layer 4 head 11, the most extreme token-0 head for this prompt
is layer 7 head 10 at 0.964, and Part 3 gives 34 Kazakh tokens against 31 Russian ones.
