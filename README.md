# GenoSense
HudsonAlpha TechChallenge

CHALLENGE 1: Visualizing Overlapping Data Between Replicate Experiments
Often a standard visualization schema for a technique is key to scientists from around the world interacting and understanding results. In this challenge, teams are asked to create a standardized visualization tool using multiple .BED files that are created when determining the likelihood of two locations within a DNA sequence physically interacting.

END PRODUCT

BED file (can omit fields other than chromosome, start, end)
- Minimum: Bed file that contains all regions that intersect with a region from another experiment.
- BONUS: Bed file that contains all regions that have a minimum level of reproducibility given parameters (MinOverlap, n, k)
- Output filename should be informative about the parameters used.

BONUS:  Graphical representation.

BONUS: How does the program scale?
- It can handle 3 bed files.  Can it handle 16 and still finish within 1 day?
