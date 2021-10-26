<div align="center">

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/dissorial/prx21_erikz/app.pyy)

_This is a TL;DR version. If you'd like to read more about anything mentioned below, head over to the [web application itself](https://share.streamlit.io/dissorial/prx21_erikz/app.py)._

# PRX21: QUANTIFIED SELF

<a href='https://www.linkedin.com/in/erik-z%C3%A1vodsk%C3%BD-126a82144/'>![LinkedIn](https://img.shields.io/badge/Erik%20Z%C3%A1vodsk%C3%BD-blue?style=for-the-badge&logo=linkedin&labelColor=blue)</a>

![sklearn](https://img.shields.io/badge/sklearn-blueviolet?style=flat-square)
![altair](https://img.shields.io/badge/altair-blueviolet?style=flat-square)
![joypy](https://img.shields.io/badge/joypy-blueviolet?style=flat-square)
![pandas](https://img.shields.io/badge/pandas-blueviolet?style=flat-square)
![numpy](https://img.shields.io/badge/numpy-blueviolet?style=flat-square)
![matplotlib](https://img.shields.io/badge/altair-blueviolet?style=flat-square)
![seaborn](https://img.shields.io/badge/seaborn-blueviolet?style=flat-square)
![streamlit](https://img.shields.io/badge/streamlit-blueviolet?style=flat-square)

![python](https://camo.githubusercontent.com/3cdf9577401a2c7dceac655bbd37fb2f3ee273a457bf1f2169c602fb80ca56f8/68747470733a2f2f666f7274686562616467652e636f6d2f696d616765732f6261646765732f6d6164652d776974682d707974686f6e2e737667)

> "The quantified self (QS) is any individual engaged in the self-tracking of any kind of biological, physical, behavioral, or environmental information."
>
> _Definition borrowed from: [The Quantified Self: Fundamental Disruption in Big Data Science and Biological Discovery](https://www.liebertpub.com/doi/10.1089/big.2012.0002)_

If you think the title of this scientific article is a little far-fetched, I agree. When I started this project at the beginning of 2021, I wouldn't have guessed that analysis of self-tracked data is actually quite common. My inspiration came from a Reddit post I stumbled upon a few years ago &ndash; someone tracked their time for an entire year and analyzed the data to understand themselves better. It seemed like an interesting idea that requires a negligible time investment in exchange for a possibly significant discovery, so I went ahead with it.

### TIME

The first major part of what I tracked is time. I divided days into 30-minute intervals and assigned each one of 15 pre-defined _time categories_, such as sleep, internet, fun, hobbies, and more.

### QUANTIFIED SELF (QS)

While `time` technically falls under `QS`, I treat the two individually because I came up with 45 variables to track in `QS`, and grouping them together with `time` would be messy. These variables are subjectively evaluated attributes of my day and include things like mood, restfulness, productivity, health problems, and others.

---

With most of the year 2021 behind us, I thought now would be a good time to delve deeper into the data I've collected and hopefully uncover otherwise hidden patterns about how I function on a daily basis. The result is this web application, which is divided into two parts: **interactive visualizations** and **predictive algorithms**.

### Interactive visualizations

`Line charts | Ridgeline plots | Heatmaps | Scatterplots | K-means clustering`

### Predictive algorithms (also interactive)

`Decision tree classifier | CN2 rule induction | Support vector machine | Multiple linear regression | K-nearest neighbors`

---

## Acknowledgements

[Prakhar Rathi](https://github.com/prakharrathi25) for the multi-page setup in Streamlit

[Avik Jain](https://github.com/Avik-Jain) for model and algorithm infographics

[This reddit post](https://www.reddit.com/r/dataisbeautiful/comments/bdf1ta/every_single_%C2%BD_hour_of_my_2018_recorded_oc/) for the initial inspiration to do this

</div>
