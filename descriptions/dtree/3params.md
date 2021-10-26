- **Maximum tree depth**: This is equivalent to `layer` in the above diagram. `None` is the default value, which means nodes are expanded until all leaves are pure or until all leaves contain less than minimum number of samples that a node must contain before splitting. Since this will result in overfitting, I recommend choosing a number between 3-6.
- **Minimum number of samples that a node must contain before splitting**: How many samples each `internal node` must contain before splitting.
- **Minimum number of samples needed for a leaf node**: Number of samples needef for a `leaf node`

