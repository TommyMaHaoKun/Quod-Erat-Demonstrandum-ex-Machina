# Literature review

Accessed 2026-11-04, Asia/Singapore.

## Exact target and attribution

Peter Occil's [revised MathOverflow question 381419](https://mathoverflow.net/q/381419)
(17 January 2021) asks whether floor(n h^2/(1-h^2))+1 degree elevations
suffice for the symmetric central Bernstein polynomial in this project.

[Will Sawin's answer 381465](https://mathoverflow.net/a/381465), posted
17 January 2021 and edited 18 January 2021, derives the exact coefficient
formula and central maximum. Its subsequent central-binomial estimate is
asymptotic. The answer's final comment also describes the bounds as approximate.

The present contribution is the finite inequality that proves the requested
upper bound, with the stronger parity refinement and an exact product criterion.
The coefficient formula and central-maximum reduction are credited to Sawin.
The elementary product inequality is proved directly and is not claimed as a
new general inequality.

## Current source checks

- [Occil's requests page](https://peteroupc.github.io/requests.html), dated
  2026-07-30, still asks the question. Its formula has a transcription error;
  the precise target here follows the revised MathOverflow question.
- [Author issue 16](https://github.com/peteroupc/peteroupc.github.io/issues/16)
  is closed but contains no proof and has no comments. The live requests page
  retains the question.
- [Bernoulli Factory Algorithms](https://peteroupc.github.io/bernoulli.html)
  discusses the height-1/2 case and links back to the same MathOverflow answer.
- [Supplemental Notes](https://peteroupc.github.io/bernsupp.html), version
  2026-10-16, gives general positivity bounds, not this finite bound.

The audit also searched equivalent formulations, the author's repository issues,
and the current OpenAI math catalogue (main commit
`4eaee87548250b2682affda7d05d947c05554bae`). No matching complete solution was
found. This catalogue check is search provenance, not a mathematical reference
in the paper.

## Search scope

Queries included the exact question number and title, Occil/Sawin with
"Bernstein degree elevation", "h^2", "floor(m)", "central binomial", and
"symmetric beta polynomial finite bound". Relevant hits led back to the
original question and the author's pages. The novelty conclusion concerns
this bounded search and the exact target.
