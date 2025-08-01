def flatten_event_map(df, column='ocel:omap'):
    return df.explode(column)
