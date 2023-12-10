import pandas as pd


def read_table_as_dataframe(worksheet, table_name, index=False, header=True):
    rng = worksheet.tables[table_name].range

    return rng.expand().options(pd.DataFrame, index=index, header=header).value


def write_dataframe(df, worksheet, rng_name, index=False):
    worksheet[rng_name].options(pd.DataFrame, header=1, index=index, expand='Table').value = df


def clear_rng(worksheet, rng_name, right_expand=True, down_expand=True):
    rng = worksheet[rng_name]

    if right_expand:
        rng = rng.expand('right')

    if down_expand:
        rng = rng.expand('down')

    rng.clear_contents()


