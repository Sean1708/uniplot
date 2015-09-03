title: 'A plot with many subplots.'
plots:
    -
    title: 'Some linear plots.'
    labels:
        x: 'x (Arb.)'
        y: 'y (Arb.)'
    axes:
        -
        x: 1, 2, 3, 4, 5, 6, 7, 8, 9
        y: 2, 4, 6, 8, 10, 12, 14, 16, 18
        --
        x: 1, 2, 3, 4, 5, 6, 7, 8, 9
        y: 3, 6, 9, 12, 15, 18, 21, 24, 27
        -
    --
    title: 'Some quadratic plots.'
    labels:
        x: 'x (Arb.)'
        y: 'y (Arb.)'
    axes:
        -
        x: 1, 2, 3, 4, 5, 6, 7, 8, 9
        y: 1, 4, 9, 16, 25, 36, 49, 64, 81
        --
        x: 1, 2, 3, 4, 5, 6, 7, 8, 9
        y: 2, 3, 6, 11, 18, 27, 38, 51, 66
        -
    -
share: no
