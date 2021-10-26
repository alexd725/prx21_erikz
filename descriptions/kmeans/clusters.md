## Elbow method

- In the chart below, the `Y axis` shows the _within-cluster sum of square (WCSS)_ distances between each point and the centroid in its cluster `k`
- If `k = 1`, WCSS will be large because some data points will inevitably be very far away from the cluster
- The larger the `k`, the lower the WCSS. If every data point had its own cluster, WCSS would equal to 0 (which would render K-means useless)
- Since there's only so many clusters your data can reasonably fall into, the goal is simple: find a point on the graph where `WCSS` starts decreasing by significantly lower amounts and begings to become parallel with the X-axis. In other words, a point where the charts makes an "elbow"
- If our graph looks like the one below, I'd choose either 3, 4, or 5 clusters
- _Side note: I think matplotlib uses linear interpolation for this chart. If it were a function instead, finding optimal `k` would probably be a pretty simple derivative problem_
