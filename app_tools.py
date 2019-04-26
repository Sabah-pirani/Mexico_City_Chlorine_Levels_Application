import plotly.graph_objs as go
import plotly.offline as ply

def get_and_plot_delegacion_data(delegacion):
    from main_app import Delegacion, Calidad, Fecha

    delegacion_row = Delegacion.query.filter_by(name=delegacion).first()
    calidad_data = Calidad.query.filter_by(delegacion_id=delegacion_row.id).all()

    neighborhoods = []                                                          # identify all distinct neighborhoods included in calidad_data
    for pt in calidad_data:
        if pt.neighborhood not in neighborhoods:
            neighborhoods.append(pt.neighborhood)

    traces = []                                                                 # create the tracees - data collections (one trace for each neighborhood)
    for neighborhood in neighborhoods:
        data = Calidad.query.filter_by(delegacion_id = delegacion_row.id).filter_by(neighborhood = neighborhood ).all()
        date = []
        average_cl_level = []
        for pt in data:
            date.append(pt.date)
            average_cl_level.append(pt.average)
        traces.append(go.Scatter(
            x = date,
            y = average_cl_level,
            name = neighborhood,
            mode = 'markers'))

    layout = go.Layout(                                                         # create layout dictionary
        title = "Chlorine Levels in Household Water Samples in "+ delegacion +" Delegacion",
        xaxis = dict(title = "Time"),
        yaxis = dict(title = "Concentration of Chlorine in [unit]")
    )

    data = []                                                                   # pack the data
    for i in range(len(traces)):
        data.append(traces[i])

    graph_data = go.Figure(data = data, layout = layout)

    plot = ply.plot(graph_data, output_type='div')                              # Create the figure

    return plot

def get_and_plot_all_data():
    from main_app import Delegacion, Calidad, Fecha

    traces = []                                                                 # create the tracees - data collections (one trace for each delegacion)
    for i in range(1,19):
        delegacion = Delegacion.query.filter_by(id = i).first()
        data = Calidad.query.filter_by(delegacion_id = i).all()

        date = []
        average_cl_level = []
        for pt in data:
            date.append(pt.date)
            average_cl_level.append(pt.average)

        traces.append(go.Scatter(
            x = date,
            y = average_cl_level,
            name = delegacion.name,
            mode = 'markers'))

    layout = go.Layout(                                                         # create layout dictionary
        title = "Chlorine Levels in Household Water Samples in Delegaciones in Mexico City",
        xaxis = dict(title = "Time"),
        yaxis = dict(title = "Concentration of Chlorine in [unit]")
    )

    data = []                                                                   # pack the data
    for i in range(len(traces)):
        data.append(traces[i])

    graph_data = go.Figure(data = data, layout = layout)

    plot = ply.plot(graph_data, output_type='div')                              # Create the figure

    return plot
