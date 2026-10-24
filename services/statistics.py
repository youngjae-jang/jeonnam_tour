"""차트에 사용할 요약 데이터."""
def counts(df, column):
    return df.groupby(column,as_index=False).size().rename(columns={'size':'count'}).sort_values('count',ascending=False)
