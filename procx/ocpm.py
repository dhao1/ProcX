from collections import defaultdict

def extract_object_traces(df, object_type_col='ocel:omap', activity_col='ocel:activity', timestamp_col='ocel:timestamp'):
    object_traces = defaultdict(list)
    for _, row in df.iterrows():
        for obj in row[object_type_col]:
            object_traces[obj].append((row[timestamp_col], row[activity_col]))
    for obj in object_traces:
        object_traces[obj] = sorted(object_traces[obj])
    return object_traces
