# Repo:    grade-book

The purpose of this code is to automate the management of a grade book.

## Description

Given the path to a file containing student scores, this code can:
* assess student improvement
* calculate curves
* calculate aggregated scores and statistics
* assign grades
* plot various metrics

The code works by separating scores into the following different categories:
* `"home-work"`
* `"exam"`
* `"extra credit"`
* `"curve"`


The user must also specify the index of each column that corresponds to a particular score or student attribute before reading in a data-file; valid extensions for the data-file include ".txt", ".csv", or ".xlsx". The image below is a screenshot of fake student names and scores that are used as an example.

![example-data](data/data_screenshot.png)

The first row (indexed by `0`) shows the maximum score for each assignment; each row below the first row corresponds to a student. The maximum scores are necessary to calculate percentages. Note that percentages are not applied to extra credit points and curve points because these are considered bonus points; this is because curves based upon improvement have unrealistic upper bounds; however, one can optionally bound the maximum possible curve. Similarly, I figured that extra credit assignments with maximum possible scores could be incorporated into the `home-work` category. The first column (indexed by `0`) shows the student name. To differentiate between missing scores and zero-scores, missing scores are denoted by NaN (Not a Number) in the data file.

One can specify the grade-boundaries; if `points_at_ace` is not provided, then the default value of the minimum number of points required to earn an $A+$ is $95$ % of the maximum possible point total (not including extra credit scores and curve scores, if provided). If `points_at_fail` is not provided, then the default value of the maximum number of points to earn a $D-$ is given as half of `points_at_ace`. One can also specify the grade-boundaries in-between `points_at_ace` and `points_at_fail`; if not provided, then the boundaries are selected to allocate an equal number of points to each sub-division. In addition to this, one can choose `side_bias="left"` (lower-bound $\leq$ score $<$ upper-bound ) or `side_bias="right"` (lower-bound $<$ score $\leq$ upper-bound ). This example uses `points_at_fail=80`, `points_at_ace=150`, and `side_bias="left"`.

This code can apply flat curves and improvement curves. A flat curve is a curve that allocates the same number of points to each student; conversely, the improvement curve is based upon the average of the weighted differences of the second-half of scores to the first-half of scores, and is calculated by multiplying this average value by a scale-factor. For this example, the home-work improvement curve would compare the second-half of scores (HW 6 $-$ 10) with the first half of scores (HW 1 $-$ 5). The final scores are recalculated each time the curves are updated or removed. When calculating curves, missing scores are treated as zero-scores.

Once the grade-book is initialized, one can view this data in a variety of plots. 

* Histogram of scores
  
  * view by particular assignment (for example, "HW 1")
  
  * view by particular categories (for example, "home-work")
  
  * view by grade
    
    <img src="output/Hist-wRUG-ByGrades.png" title="" alt="example-histogram_grades" data-align="center">

* Heat-map of score differences
  
  * view by particular assignment
  
  * view by particular categories
  
  * view by total

<img src="output/HeatMap-HW_1_HW_2_HW_3_HW_4_HW_5_HW_6_HW_7_HW_8_HW_9_HW_10_Quiz_Test_flat_curve_home_work_improvement_curve_exam_improvement_curve-ByPoints.png" title="" alt="example-heat_map" data-align="center">

* Box-plot of score statistics
  
  * view by particular assignment
  
  * view by particular categories
  
  * view by total
  
  * view statistics by points or by percentage (useful if assignments or categories are weighted differently)

<img src="output/BoxPlot-HW_1_HW_2_HW_3_HW_4_HW_5_HW_6_HW_7_HW_8_HW_9_HW_10_Quiz_Test_flat_curve_home_work_improvement_curve_exam_improvement_curve-ByPoints.png" title="" alt="example-box_plot" data-align="center">

* Cumulative bar-stacks
  
  * view by particular assignment or by particular categories

<img src="output/BarStack-wDIFF-HW_1_HW_2_HW_3_HW_4_HW_5_HW_6_HW_7_HW_8_HW_9_HW_10_Quiz_Test_flat_curve_home_work_improvement_curve_exam_improvement_curve-ByPoints.png" title="" alt="example-cumumlative_bar_stacks" data-align="center">

* Polar charts
  
  * view grades distribution as:
    
    * pie-chart
    
    * donut-chart
    
    * annular chart

<img src="output/PolarChart-Annulus-ByGrades.png" title="" alt="example-polar_chart" data-align="center">

* Table
  
  * view table of data with point totals and grades
  
  * output the updated dataframe

<img src="output/Table-woSWAP-ByGrades.png" title="" alt="example-table_grades" data-align="center">

## Getting Started

### Dependencies

* Python 3.9.6
* numpy == 1.26.4
* matplotlib == 3.9.4
* pandas == 2.2.3
* collections (default)

### Executing program

* Download this repository to your local computer

* Modify `path_to_data` and `path_to_save_directory` in `src/example_01-back_end.py` and then run the script

## Version History

* 0.1
  * Initial Release

## To-Do

* modify heat-maps by either transforming 2-D data or by moving xticklabels from bottom x-axis to top x-axis

* fix `missing number student scores` in legend of heat-maps

* use different color-map for each category of scores in plots of cumulative bar-stacks

* add email functionality

* add gui

## License

This project is licensed under the Apache License - see the LICENSE file for details.
