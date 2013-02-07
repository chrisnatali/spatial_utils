# Perform segment intersection with point, line and rectangle

area2 <- function(a, b, c) {
     return (((b[1] - a[1]) * (c[2] - a[2])) - ((c[1] - a[1]) * (b[2] - a[2])))
}

left <- function(a, b, c) {
    return (area2(a, b, c) > 0)
}

collinear <- function(a, b, c) {
    return (area2(a, b, c) == 0)
}

# Proper intersection (i.e. if an endpoint lies on the other line, it's NOT a proper intersection)
intersects_prop <- function(a, b, c, d) {
    if ( collinear(a, b, c) || collinear(a, b, d) ||
         collinear(c, d, a) || collinear(c, d, b)) {
        return (FALSE)
    }
    return ( xor(left(a, b, c), left(a, b, d)) &&
             xor(left(c, d, a), left(c, d, b)))
}

# Check whether c is between a and b
between <- function(a, b, c) {
    if ( !collinear(a, b, c)) {
        return(FALSE)
    }

    if (a[1] != b[1]) { # not vertical case, we can compare on x axis
        return (
            ((a[1] <= c[1]) && (c[1] <= b[1])) ||
            ((a[1] >= c[1]) && (c[1] >= b[1])))
    } else { # a and b are a vertical segment, we need to compare on y axis
        return (
            ((a[2] <= c[2]) && (c[2] <= b[2])) ||
            ((a[2] >= c[2]) && (c[2] >= b[2])))
    }
}

# includes improper case (i.e. endpoint's count)
intersects <- function(a, b, c, d) {
    if (intersects_prop(a, b, c, d)) {
        return (TRUE)
    } else if ( between(a, b, c) || between(a, b, d) ||
                between(c, d, a) || between(c, d, b) ) {
        return (TRUE)
    } else { return (FALSE) }
}

lineIntersectsRegion <- function(a, b, ll, ur) {
    ul = c(ll[1], ur[2])
    lr = c(ur[1], ll[2])
    return (intersects(ll, ul, a, b) || intersects(ul, ur, a, b) ||
            intersects(ur, lr, a, b) || intersects(lr, ll, a, b))
}
