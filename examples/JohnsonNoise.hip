title: 'The dependence of Johnson noise on bandwidth.'
labels:
    x: 'Bandwidth (Hz)'
    y: '$V^2 (V^2)$'
axes:
    -
    x:
        values: 333, 355, 784, 1000, 1051, 1077, 2576, 3332, 3554
        errors: 0.05
    y:
        values: 5.4e-14, 5.4e-14, 1.28e-13, 1.64e-13, 1.75e-13, 1.75e-13, 4.33e-13, 5.47e-13, 5.92e-13
        errors: 3e-15,   3e-15,   4e-15,    4e-15,    3e-15,    4e-15,    6e-15,    6e-15,    8e-15
    --
    x: 'examples/JNoiseBandwidthDependence.csv:0:1'
    y: 'examples/JNoiseBandwidthDependence.csv:1:1'
    -
