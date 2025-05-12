# Introduction
Irolling is a tiny tool for analysing the backwardation of stock index future and providing suggestion for rolling contract.

Thanks to the hedging from market neutral strategy, backwardation is a special and eligible alpha gift for individual investors.

# Install

```
$ git clone git@github.com:DeliangFan/irolling.git
$ cd irolling
$ python setup.py install
```

# Usage

List the basis for current contracts.

```
$ irolling list
Compute basis with daily 20250512
+--------+----------------+------------+---------+----------------+------------------------+-------------------------+
| Symbol | Contract Price | Spot Price |  Basis  | Basis Ratio(%) | Basis Ratio By Year(%) | Residual Maturity(days) |
+--------+----------------+------------+---------+----------------+------------------------+-------------------------+
| IH2505 |     2703.8     |  2702.62   |   1.18  |      0.04      |          3.98          |            4            |
| IH2506 |     2686.6     |  2702.62   |  -16.02 |     -0.59      |         -5.55          |            39           |
| IH2509 |     2653.2     |  2702.62   |  -49.42 |     -1.83      |         -5.13          |           130           |
| IH2512 |     2649.0     |  2702.62   |  -53.62 |     -1.98      |         -3.28          |           221           |
| IF2505 |     3885.0     |  3890.61   |  -5.61  |     -0.14      |         -13.16         |            4            |
| IF2506 |     3853.0     |  3890.61   |  -37.61 |     -0.97      |         -9.05          |            39           |
| IF2509 |     3786.6     |  3890.61   | -104.01 |     -2.67      |         -7.51          |           130           |
| IF2512 |     3749.6     |  3890.61   | -141.01 |     -3.62      |         -5.99          |           221           |
| IC2505 |     5786.0     |  5793.67   |  -7.67  |     -0.13      |         -12.08         |            4            |
| IC2506 |     5688.0     |  5793.67   | -105.67 |     -1.82      |         -17.07         |            39           |
| IC2509 |     5524.6     |  5793.67   | -269.07 |     -4.64      |         -13.04         |           130           |
| IC2512 |     5417.8     |  5793.67   | -375.87 |     -6.49      |         -10.71         |           221           |
| IM2505 |     6151.6     |  6167.46   |  -15.86 |     -0.26      |         -23.47         |            4            |
| IM2506 |     6037.0     |  6167.46   | -130.46 |     -2.12      |         -19.8          |            39           |
| IM2509 |     5843.4     |  6167.46   | -324.06 |     -5.25      |         -14.75         |           130           |
| IM2512 |     5702.2     |  6167.46   | -465.26 |     -7.54      |         -12.46         |           221           |
+--------+----------------+------------+---------+----------------+------------------------+-------------------------+
```

For more usage, you may refer to

```
$ irolling -h
```