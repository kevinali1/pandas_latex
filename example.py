import pandas as pd
from pandas_latex.utils import treat_column, build_table

df = pd.read_csv('testdata.csv')
df['Stock'] = treat_column(df['Stock'], is_data_column=False)
df['Country'] = treat_column(df['Country'], is_data_column=False)
df['30D Ret.'] = treat_column(df['30D Ret.'], is_data_column=True, as_percent=True)
df['3M Ret.'] = treat_column(df['3M Ret.'], is_data_column=True, as_percent=True)
df['6M Ret.'] = treat_column(df['6M Ret.'], is_data_column=True, as_percent=True)
df['12M Ret.'] = treat_column(df['12M Ret.'], is_data_column=True, as_percent=True)
df['12M Chart'] = treat_column(df['12M Chart'], is_data_column=True, as_percent=True)

testfile = open('industry_right_testing.tex', 'r')
testdata = testfile.read()
testfile.close()

output_table = build_table(df,
                           heading_widths=[0.3, 0.1, 0.075, 0.07, 0.07, 0.08, 0.15],
                           heading_font="DATAHEAD",
                           table_font="DATASMALL",
                           table_color="regulargrey",
                           line_color="lightgrey")

with open('industry_right_out.tex', 'w') as myfile:
    myfile.write(testdata.replace("MY_LONGTABLE", output_table))
