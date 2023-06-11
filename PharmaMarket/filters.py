from PharmaMarket import app


@app.template_filter('format_data')
def format_data(value):
    if isinstance(value, int):
        return str(value)
    else:
        return value.replace('_', ' ').capitalize()


