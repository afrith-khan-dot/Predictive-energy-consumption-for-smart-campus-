# Data Quality Report - Phase 1

**Available Sheets**: July, August, September, All Data

Selected '**All Data**' as the consolidated dataset.

**Original Row Count**: 79
**Original Column Count**: 13
**Columns**: Month, Date, TNEB Campus HTSC-91, TNEB New STP HTSC-178, Power Generation by Solar Panels, Power Generation by Diesel Engines, Power Generation by Biogas Engines, Staff Quarters, Academic blocks, Hostels, Chiller plant, STP, Total Consumption

### Data Types
- `Month`: object
- `Date`: datetime64[ns]
- `TNEB Campus HTSC-91`: float64
- `TNEB New STP HTSC-178`: float64
- `Power Generation by Solar Panels`: float64
- `Power Generation by Diesel Engines`: float64
- `Power Generation by Biogas Engines`: float64
- `Staff Quarters`: float64
- `Academic blocks`: float64
- `Hostels`: float64
- `Chiller plant`: object
- `STP`: float64
- `Total Consumption`: float64


**Duplicate Rows**: 5

### Missing Values (Original)
- `Month`: 6
- `Date`: 6
- `TNEB Campus HTSC-91`: 6
- `TNEB New STP HTSC-178`: 6
- `Power Generation by Solar Panels`: 6
- `Power Generation by Diesel Engines`: 6
- `Power Generation by Biogas Engines`: 6
- `Staff Quarters`: 6
- `Academic blocks`: 6
- `Hostels`: 6
- `Chiller plant`: 6
- `STP`: 6
- `Total Consumption`: 6


**Note**: Found 6 completely empty rows at the end of the dataset. These will be removed.

**Chiller Plant Issues**: Found non-numeric values. Example: ['2790 (2)' '5901(1)']. Coercing to numeric.

**STP Column Analysis**: After empty-row removal and linear interpolation, missing values in STP: 0.

**Date Range**: 2026-07-01 to 2026-09-11

### Total Consumption Validation
- Max difference vs Generation Sum: 9108.0
- Max difference vs Infrastructure Consumption Sum: 2507.0
Conclusion: 'Total Consumption' does not perfectly equal the sum of generating sources or consuming infrastructure in every row. It should be used as the primary target variable, but discrepancies exist in the dataset.

### Numeric Summary Statistics
```text
                      Date  TNEB Campus HTSC-91  TNEB New STP HTSC-178  Power Generation by Solar Panels  Power Generation by Diesel Engines  Power Generation by Biogas Engines  Staff Quarters  Academic blocks       Hostels  Chiller plant          STP  Total Consumption
count                   73            73.000000              73.000000                         73.000000                           73.000000                           73.000000       73.000000        73.000000     73.000000      73.000000    73.000000          73.000000
mean   2026-08-06 00:00:00         18446.849315             810.082192                       4860.835616                          274.863014                          546.698630     1960.589041     10846.917808   7030.835616    3638.698630  1353.356164       24754.342466
min    2026-07-01 00:00:00          8460.000000             532.000000                       1868.000000                            0.000000                           77.000000     1738.000000      6929.000000    769.000000       0.000000   896.000000       13203.000000
25%    2026-07-19 00:00:00         15440.000000             718.000000                       4001.000000                            0.000000                          421.000000     1892.000000      9148.000000   6345.000000    2419.000000  1254.000000       21570.000000
50%    2026-08-06 00:00:00         19900.000000             790.000000                       4926.000000                            0.000000                          528.000000     1961.000000     11432.000000   6979.000000    4314.000000  1364.000000       25540.000000
75%    2026-08-24 00:00:00         21420.000000             906.000000                       5735.000000                          160.000000                          671.000000     2035.000000     12144.000000   7805.000000    4860.000000  1456.000000       27860.000000
max    2026-09-11 00:00:00         26620.000000            1388.000000                       6801.000000                         5192.000000                         1032.000000     2239.000000     16384.000000  10362.000000    6874.000000  1720.000000       34038.000000
std                    NaN          4144.219829             148.952803                       1098.725866                          755.583059                          190.822247      114.680212      2070.958130   1813.256486    1966.516808   160.972252        4563.451013
```
