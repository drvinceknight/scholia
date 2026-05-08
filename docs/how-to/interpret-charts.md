# Interpret the charts

Running `scholia mark` saves a set of charts to `scholia/charts/`.
Each chart addresses a different question about the cohort.

## Mark distribution (`distribution.png`)

A histogram of students' total marks. The x-axis is the total mark and
the y-axis is the number of students. This gives the quickest read of
where the cohort sits and whether the marks are concentrated or spread
out.

## Per-question mark distribution (`per_question.png`)

One bar chart per question, showing how many students received each
mark value for that question. A chart dominated by a single bar
indicates that most students fell into the same category, which may
signal that the question was too easy, too hard, or poorly calibrated.

## Cumulative mark distribution (`cumulative.png`)

The cumulative proportion of students at or below each total mark. The
y-axis runs from 0 to 1. This chart is useful for checking grade
boundaries: reading off the curve at a given mark shows immediately what
fraction of the cohort falls below it.

## Marks per question (`boxplot.png`)

Side-by-side boxplots of the mark distribution for each question. The
box covers the interquartile range, the line inside is the median, and
the whiskers extend to the data extremes. Comparing boxes across
questions shows which questions produced the most variation and which
were marked similarly across the cohort.

## Question mark correlations (`correlation.png`)

A heatmap of the Pearson correlation between question marks. Each cell
shows the correlation between one pair of questions, ranging from
-1 (perfect negative) to +1 (perfect positive). A high positive
correlation between two questions suggests they are measuring related
skills. A low or negative correlation suggests the questions are
relatively independent.

This chart is only generated when there are at least two questions and
at least two fully-marked students. With small cohorts (fewer than
roughly 15 students) the values should be interpreted cautiously.
