
def to_excel_autowidth_and_border(writer, df, sheetname, startrow, startcol):
    df.to_excel(
        writer, sheet_name=sheetname, index=False, startrow=startrow, startcol=startcol
    )  # send df to writer
    workbook = writer.book
    worksheet = writer.sheets[sheetname]  # pull worksheet object
    formater = workbook.add_format({"border": 1})
    for idx, col in enumerate(df):  # loop through all columns
        series = df[col]
        max_len = (
                max(
                    (
                        series.astype(str).map(len).max(),  # len of largest item
                        # series.map(len).max(),
                        len(str(series.name)),  # len of column name/header
                    )
                )
                * 3
                + 1
        )  # adding a little extra space
        # print(max_len)
        worksheet.set_column(
            idx + startcol, idx + startcol, max_len
        )  # set column width
    first_row = startrow
    first_col = startcol
    last_row = startrow + len(df.index)
    last_col = startcol + len(df.columns)
    worksheet.conditional_format(
        first_row,
        first_col,
        last_row,
        last_col - 1,
        options={"type": "formula", "criteria": "True", "format": formater},
        )