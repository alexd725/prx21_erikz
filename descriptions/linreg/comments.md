- **Short answer:** It's complicated
- **Short but honest answer:** I'm not entirely sure
- **Short and likely the correct answer:** Probably not

### Long answer: there's several problems with using regression here:

- Not even the `time` variables I track are truly continuous. Yes, time itself is continuous, but since I track everything in 30-minute intervals, all time variables can take on only 48 different values (30m, 1h, 1h30m, etc.) &ndash; not very continous. This way they're at least ordinal, which I think is good enough
- `QS` variables can only take on 5 different values when I track them, but they're treated as continuous here (why you can choose them as a `target` is explained below)
- There's no clear way for me to distinguish between independent, dependent and confounding variables in my dataset (aside from `supplements`, which I'd consider independent). The same problem is true for every model on this web app
- I can't always choose what to spend my time on, let alone how much
- Everything sort of affects...well, everything
