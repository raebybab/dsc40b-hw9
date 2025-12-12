# min_ell_theta.py
#
# Programming Problem 2: Parts (a)–(d)
#
# All required functions are implemented in this single file.


# -----------------------------------------------------------
# Part (a)
# -----------------------------------------------------------
def learn_theta(data, colors):
    """
    Given that ALL blue points are < ALL red points, return a θ such that:
        blue ≤ θ  and  red > θ

    A valid θ is any value strictly between:
        max_blue_value and min_red_value
    """

    max_blue = None
    min_red = None

    for x, c in zip(data, colors):
        if c == 'blue':
            if max_blue is None or x > max_blue:
                max_blue = x
        else:  # red
            if min_red is None or x < min_red:
                min_red = x

    # Return midpoint
    return 0.5 * (max_blue + min_red)



# -----------------------------------------------------------
# Part (b)
# -----------------------------------------------------------
def compute_ell(data, colors, theta):
    """
    Return loss L(theta):
        L(theta) = (# of red points ≤ θ) + (# of blue points > θ)
    Runs in Θ(n).
    """
    loss = 0
    for x, c in zip(data, colors):
        if c == 'red' and x <= theta:
            loss += 1
        elif c == 'blue' and x > theta:
            loss += 1

    return float(loss)



# -----------------------------------------------------------
# Part (c) — Quadratic time implementation
# -----------------------------------------------------------
def minimize_ell(data, colors):
    """
    Return a θ minimizing L(θ). Quadratic time allowed.

    Candidate θ values can be chosen between any pair of data points.
    A simple correct method:
        For every i, choose θ = data[i] and compute loss.
    """

    n = len(data)
    best_theta = data[0]
    best_loss = compute_ell(data, colors, data[0])

    for i in range(n):
        theta = data[i]
        loss = compute_ell(data, colors, theta)
        if loss < best_loss:
            best_loss = loss
            best_theta = theta

    return float(best_theta)



# -----------------------------------------------------------
# Part (d) — Linear-time algorithm assuming data is sorted
# -----------------------------------------------------------
def minimize_ell_sorted(data, colors):
    """
    data is sorted; colors[i] corresponds to data[i].
    Exactly n/2 are red and n/2 are blue.
    Return θ minimizing L(θ) in Θ(n) time.

    Loop invariant:
        After the α-th iteration, blue_gt_theta is the number of blue
        points with value > data[α - 1].
    """

    n = len(data)

    # Precompute: total number of red ≤ θ initially (θ < all data)
    red_le = 0
    blue_gt = colors.count('blue')  # initially, θ is −∞ → all blues counted

    best_loss = red_le + blue_gt
    best_theta = data[0]  # any θ before the first data point

    # Sweep over positions where θ = data[i]
    for i in range(n):
        # When θ passes data[i], update red_le and blue_gt accordingly
        if colors[i] == 'red':
            red_le += 1
        else:
            blue_gt -= 1

        loss = red_le + blue_gt
        if loss < best_loss:
            best_loss = loss
            best_theta = data[i]

    return float(best_theta)