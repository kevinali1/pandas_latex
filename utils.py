import pandas as pd

BAD_CHARS = "&%$#_{}"


def escape_chars(input_text):
    output = input_text
    for character in BAD_CHARS:
        output = output.replace(character, '\%s' % character)
    return output


def treat_column(input_column_as_list,
                 is_data_column,
                 num_decimals=2,
                 green_color="green",
                 red_color="red",
                 regular_color="regulargrey",
                 grey_color="mediumgrey",
                 blank_fill="NA",
                 as_percent=False):
    output = []

    if as_percent is True:
        append_symbol = "\%"
    else:
        append_symbol = ""

    for cell in input_column_as_list:
        if pd.isnull(cell):
            output.append("\color{%s} " % grey_color + blank_fill)
        else:
            if is_data_column is True:

                # Round data
                if num_decimals == 0:
                    cell_string = str("%.0f" % cell)
                elif num_decimals == 1:
                    cell_string = str("%.1f" % cell)
                elif num_decimals == 2:
                    cell_string = str("%.2f" % cell)
                else:
                    raise NotImplementedError("Unspecified number of decimals: %s" % str(num_decimals))

                # Color data
                if cell > 0:
                    output.append("\color{%s} +" % green_color + cell_string + append_symbol)
                elif cell < 0:
                    output.append("\color{%s} " % red_color + cell_string + append_symbol)
                elif cell == 0:
                    output.append("\color{%s} " % grey_color + cell_string + append_symbol)
                else:
                    raise NotImplementedError("Unknown treatment for data: " + str(cell))
            else:
                output.append("\color{%s} " % regular_color + escape_chars(cell))

    return output


def build_table(df,
                heading_widths=None,
                heading_font=None,
                table_font=None,
                table_color=None,
                line_color=None):

    num_columns = len(df.columns)

    if heading_widths is None:
        heading_widths = [1.0/num_columns for column in df.columns]
    assert(len(heading_widths) == len(df.columns))

    if heading_font is None:
        heading_font = ""
    if table_font is None:
        table_font = ""

    # Set column widths
    output = "\\begin{longtable}"
    output += "{%s}" % ("|".join(["p{%s\\textwidth}" % escape_chars(str(heading_width)) for heading_width in heading_widths])) + "\n"

    # Set line color
    if line_color is not None:
        output += "\\arrayrulecolor{%s}\n" % line_color

    # Set table color
    if table_color is not None:
        output += "\color{%s}\n" % table_color

    # Build header row
    header_row = " & ".join(["\\" + heading_font + " " + escape_chars(column_name) for column_name in df.columns]) + " \\\ \hline \n\endfirsthead \n"
    output += header_row

    # Build data rows
    for index in df.index:
        data_row = " & ".join(["\\" + table_font + " " + celldata for celldata in df.ix[index]]) + " \\\ \hline \n"
        output += data_row

    # End table
    output += "\n \hline \n"
    output += " \end{longtable}"

    return output
