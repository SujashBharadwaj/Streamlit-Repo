---
title: Gradient descent: a visual guide and playground
date: 2025-09-08
---

# Gradient descent: a visual guide and playground

Published: Sep 8, 2025 ~10 min read

 One line summary: follow the negative gradient to move downhill on a cost function until the slope is close to zero.
 

## History

 Augustin-Louis Cauchy wrote one of the first clear accounts of the steepest-descent method in 1847 while studying how to minimize functions using derivatives. The idea is simple: from your current point, move in the direction where the function drops fastest, choose a sensible step, and repeat. The method spread from numerical analysis to optimization and then to machine learning.
 

 Modern variants like stochastic and mini-batch gradient descent, momentum, RMSProp, and Adam drive the training of large neural networks. The common thread is the same Cauchy intuition: slope tells you which way to go.
 

![Portrait of Augustin-Louis Cauchy](../assets/img/cauchy.png)

 Cauchy (1789–1857). His steepest-descent rule mixes two ingredients: a direction from the derivative and a step length from a simple search. This mix is still what we use today.
 

## Why was it proposed?

 The task is to find a parameter value that makes a differentiable function \(f(\theta)\) as small as possible. In many problems you cannot solve \(f'(\theta)=0\) in closed form, the function may be high dimensional, and each evaluation can be noisy or expensive. Steepest descent gives a local, iterative recipe that only needs gradients. It uses a first-order Taylor approximation around the current point and takes a step that reduces the value for a small enough learning rate. That makes it cheap to compute, easy to code, and predictable to improve.
 

## How it works (math)

 In one dimension the update is
 \( x\_{t+1} = x\_t - \alpha\, f'(x\_t) \).
 In more than one dimension we write
 \( \boldsymbol{\theta}\_{t+1} = \boldsymbol{\theta}\_t - \alpha\, \mathrm{grad}\, f(\boldsymbol{\theta}\_t) \).
 The learning rate \( \alpha \) controls how far you step. Small \( \alpha \) gives slow progress. Large \( \alpha \) can overshoot or diverge.
 

 A quick justification uses the first-order approximation
 \( f(\theta+\Delta) \approx f(\theta) + \mathrm{grad}\,f(\theta)^\top \Delta \).
 Choosing \( \Delta = -\alpha\, \mathrm{grad}\, f(\theta) \) gives a decrease for small \( \alpha \).
 On a round quadratic the path heads straight to the minimum.
 On a narrow valley the path zig-zags unless you add momentum or scale the features.
 

![Bowl shaped curve with a tangent and the downhill direction](../assets/img/bowltangent.png)

 A bowl shaped \(f(x)\). The tangent shows the local slope. Gradient descent takes a step in the opposite direction. With a good step size you move toward the bottom each time.
 

## Interactive playground (1-D, cubic only)

Define a cubic \(f(x)=a\_3x^3+a\_2x^2+a\_1x+a\_0\). Pick a learning rate and a start point. We round each step to 2 decimals and stop at 20 iterations.

Coefficients

Initial \(x\_0\)

Learning rate \(\\alpha\)

 Round each step to 2 decimals

Override derivative \(f'(x)\) (optional)

Use x, numbers, +, −, *, ^. Example: 3x^2 − 2x + 1.

Step once
Run to 20 or convergence
Reset

We stop early if \(|f'(x)| < 0.01\). If 20 steps are reached we report the last value.

| Step | x | f(x) | f'(x) |
| --- | --- | --- | --- |

### Desmos view

## Usage in machine learning

 We use gradient descent whenever we fit parameters by minimizing a loss. Linear regression uses mean squared error. Logistic regression uses log loss. Neural networks minimize a sum of per example losses composed with layers of nonlinear functions. In large datasets we rarely use the full gradient every time. Stochastic gradient descent computes a noisy gradient from a small batch and takes many cheap steps. Momentum speeds travel along valleys and reduces zig-zags. Methods like AdaGrad, RMSProp, and Adam adapt step sizes per parameter using running statistics of past gradients. Regularization terms such as L1, L2, or weight decay are added to the objective and included in the update.
 

![3D cost surface with a descent path](../assets/img/3Dcostsurface.png)

 Complex surfaces can have several valleys. Different starting points may reach different minima. Schedules and momentum help keep progress steady.
 

## Limitations

* **Local view only.** It can stop at a local minimum or a saddle point.
* **Step size is delicate.** Too small is slow, too large overshoots or diverges.
* **Ill-conditioning.** Narrow valleys cause zig-zags. Feature scaling or preconditioning helps.
* **Noisy gradients.** With mini-batches the path wanders. Use schedules to cool the learning rate.
* **Non-differentiable points.** Kinks need subgradients or smoothing.
* **Slow near the minimum.** Slopes are tiny. Momentum or second-order ideas help finish.

## Conclusion

 Gradient descent lasts because it is practical. It needs a differentiable objective and a learning rate. With those two pieces it scales from a single variable to very large models. When you can write a loss and its gradient, you can try gradient descent in a few lines and usually get something that learns. Schedules, momentum, and adaptive steps are refinements on the same loop.
 

## Fun facts

* Cauchy described steepest descent with a simple line search to pick step size.
* Early texts called it steepest descent or method of slopes. The word “gradient” came later.
* On a quadratic with a perfect step size, one step can hit the minimum.
* Feature scaling can turn a zig-zag path into a straight shot.
* Most deep learning optimizers are gradient descent with smarter step sizes and momentum memories.

[Back to Blog](../blog/)
