import loacore.load.file_load as file_load
files = file_load.load_database(load_deptrees=False)

import loacore.analysis.sentiment_analysis as sentiment_analysis
polarities = sentiment_analysis.compute_extreme_files_polarity(files, pessimistic=False)

import loacore.utils.plot_pies as plot_pies
plot_pies.plot_polarity_pie_charts(polarities)