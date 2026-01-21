---
title: Means in statistics: definitions, formulas, history, and when to use each
date: 2025-09-02
---

# Means in statistics: definitions, formulas, history, and when to use each

Published: Sep 2, 2025

 For positive data it is useful to remember this order: Harmonic ≤ Geometric ≤ Arithmetic ≤ RMS ≤ Contraharmonic. Each mean tells a different story about the same numbers.
 

## Core definitions and formulas

### Arithmetic Mean

**Definition.** The simple average of values. It shares the total evenly across all observations.

**Formula.** \( \displaystyle \bar{x}=\frac{1}{n}\sum\_{i=1}^{n}x\_i \)

**History.** The idea of averaging appears in ancient arithmetic practice and became standard in early modern statistics as a basic summary. It is tied to the method of least squares since minimizing squared errors targets the arithmetic mean as a center. The mean entered official statistics through astronomy and geodesy where repeated measurements were combined. In the twentieth century it became the default figure in reports and dashboards. Its popularity comes from linearity and ease of interpretation. Its weakness is sensitivity to outliers and skew.

### Geometric Mean

**Definition.** The multiplicative average. It describes a typical proportional change.

**Formula.** \( \displaystyle \operatorname{GM}(x)=\Big(\prod\_{i=1}^{n}x\_i\Big)^{1/n} \) with \(x\_i>0\)

**History.** The geometric mean appears in Greek geometry and later in Euclid’s right-triangle altitude theorem. It became important in finance and growth analysis because compounding is multiplicative. Scientists use it for fold changes and ratios where units cancel. In information retrieval and model scoring it stabilizes chained rates. Its use spread with logarithms because logs turn products into sums. The key restriction is that values must be positive.

### Harmonic Mean

**Definition.** The correct average for rates and ratios per unit.

**Formula.** \( \displaystyle \operatorname{HM}(x)=\frac{n}{\sum\_{i=1}^{n}1/x\_i} \) with \(x\_i>0\)

**History.** The harmonic mean was studied with the arithmetic and geometric means in classical mathematics. It fits problems where distance or work is fixed and speed varies. Statisticians adopted it for combined rates and effective resistances in physics. In modern metrics like the F1 score it balances precision and recall by penalizing small components. It is sensitive to zeros and requires strictly positive inputs. When small values matter a lot, HM is the honest center.

### RMS (Quadratic Mean)

**Definition.** The magnitude average based on squares. It emphasizes large deviations.

**Formula.** \( \displaystyle \operatorname{RMS}(x)=\sqrt{\frac{1}{n}\sum\_{i=1}^{n}x\_i^2} \)

**History.** RMS rose with electrical engineering and statistical error analysis. Alternating current power is proportional to the square of voltage or current, which makes RMS natural. In statistics RMS appears inside variance and root mean square error. In signal processing it measures energy and loudness. As squaring inflates large values, RMS sits above the arithmetic mean for positive data. It is the \(p=2\) case of the power mean family.

### Contraharmonic Mean

**Definition.** An intensity-weighted average that favors large values.

**Formula.** \( \displaystyle C(x)=\frac{\sum\_{i=1}^{n}x\_i^2}{\sum\_{i=1}^{n}x\_i} \) with \(x\_i\ge 0\) and \( \sum x\_i>0 \)

**History.** The contraharmonic mean appears in classical number theory and is closely related to the Lehmer means. It has practical uses in image filtering where brighter pixels carry more weight. In size-biased sampling it upweights larger units. Because the numerator uses squares it can move far to the right when large values are present. It sits above RMS for strictly positive and spread out data. It is best used when large intensities should drive the average.

### Weighted Mean

**Definition.** A mean that respects different importances or sample sizes.

**Formula.** \( \displaystyle \bar{x}\_w=\frac{\sum\_{i=1}^{n}w\_i x\_i}{\sum\_{i=1}^{n}w\_i} \) with \( \sum w\_i>0 \)

**History.** Weighted means entered statistics through survey design and meta analysis. Grades and GPAs also use credits as weights. In experiments we weight observations by precision or sample size to form combined estimates. In modern evaluation pipelines weights reflect traffic share or class importance. The figure remains easy to explain because it is still linear. Choosing weights is the main modeling decision.

### Trimmed Mean

**Definition.** The arithmetic mean after dropping a fixed percentage from each tail.

**Formula.** Sort the data, remove \(p\%\) from the bottom and top, then compute \( \bar{x} \)

**History.** Trimmed means grew out of robust statistics to reduce the pull of outliers. Statistical agencies use trimmed means to track underlying trends in volatile series. In competitions and judging they help ignore extreme scores. Analysts use them when the median throws away too much and the mean is too sensitive. The trimming level sets the robustness. A small trim gives a gentle safeguard.

### Power Mean (Generalized Mean)

**Definition.** A one-parameter family that moves from HM to GM to AM to RMS as the parameter increases.

**Formula.** \( \displaystyle M\_p(x)=\left(\frac{1}{n}\sum\_{i=1}^{n}x\_i^{\,p}\right)^{\!1/p} \) with the limits \( M\_{-1}=\mathrm{HM} \), \( \lim\_{p\to 0}M\_p=\mathrm{GM} \), \( M\_{1}=\mathrm{AM} \), \( M\_{2}=\mathrm{RMS} \)

**History.** The generalized mean collects many classical means under one roof. It explains the ordering on positive data and gives a clean way to study sensitivity. By tuning \(p\) we can reward small values or large values as needed. It shows how design choices lead to different centers. The family connects to Hölder and Minkowski inequalities. It is a good teaching tool because it makes the landscape visible.

## When to use what

| Situation | Use | Reason |
| --- | --- | --- |
| Totals or additive processes | Arithmetic mean | Shares the total evenly and is linear |
| Compounded growth or chained ratios | Geometric mean | Captures proportional change and is scale free |
| Rates over a fixed resource | Harmonic mean | Averages per unit correctly and punishes small rates |
| Energy, magnitude or squared error | RMS | Squares highlight large deviations and match power |
| Intensity or size biased contexts | Contraharmonic | Weights by the square and follows the bright or large |
| Different importances or sample sizes | Weighted mean | Reflects credits, prevalence or precision |
| Outliers present but keep a mean | Trimmed mean | Removes tails and keeps a familiar average |
| Sensitivity study or policy knob | Power mean | Move \(p\) to compare centers and see the effect |

## Interactive playground

Numbers (comma, space or newline)
1, 2, 8

Weights (optional; same count)

Trim percent each tail

Power mean \(p\) (0 gives GM, 1 gives AM, 2 gives RMS)

p = 1

Show on chart

 AM
 GM
 HM
 RMS
 Contra
 Weighted
 Trimmed
 \(M\_p\)

Compute and draw

| Mean | Value | Difference from AM |
| --- | --- | --- |

 Notes. GM and HM and \(M\_p\) with \(p\le 0\) require all values to be positive. Contraharmonic needs non-negative values and a positive sum.
 

## Takeaways

* Say which mean you used and why. The choice changes the story.
* Use geometric mean for growth and chained ratios. Use harmonic mean for rates. Use RMS when energy or large deviations matter.
* Trim if outliers dominate but you still want a mean. Report the trim level.
* Try the power mean slider to see how conclusions shift with \(p\).

[Back to Blog](../blog/)
