# Overview

The CN2 rule induction algorithm is a classification technique designed for the efficient induction of simple, comprehensible rules in the form of _if **cond** then predict **class** _.

From the variables I track, I decided to demonstrate `mood` and `time spent awake` here for several reasons:

- They seem like fairly dependent variables to me
- It's not immediately clear to me what could increase or decrease either of the two (unlike `increase in sleep = higher restfulness score`)

**_Wait, you said this is a classification algorithm but `time spent awake` is a numerical variable measured in hours and minutes._**

- I discretized this variable into 5 categories (intervals) based on equal frequency (number of data instances).

**_When I choose `mood`, why isn't there a rule set for Mood=5?_**

- Because there simply hasn't been a day where I truly felt like assigning a score of `5` to `mood`. Although I've felt great on many days this year, I suppose this has more to do with avoiding "extreme" responses, which is a common problem with Likert scales. Don't worry about me though &ndash; there's plenty of `4s`.

**_Which of all the variables you track did you use as features for this algorithm?_**

- All of them except for those in `health` and `self-related` categories because they're dependent variables. If the CN2 algorithms tells me `IF restfulness=5 THEN hobbies => 4.75h`, that's not very helpful. I can't will myself into being fully rested in order to spend more time on hobbies.

---

## Model parameters

- **Rule ordering**: _unordered_
  - Rules are learned for each class individually
- **Covering algorithm**: _exclusive_
- **Evaluation measure**: _Laplace's method_
- **Beam width**: _5_
  - Beam width is a fixed number of monitored alternatives after the best rule is learned thus far
- **Minimum rule coverage**: _21_
  - I set this sort of arbitrarily, but a rule set that holds true for at least 21 days seemed like a good starting point
- **Maximum rule length**: _8_
  - I tried experimenting with other lengths but this seemed like a balance of feasibility and specificity (should I decide to apply these rules in real life)

---
