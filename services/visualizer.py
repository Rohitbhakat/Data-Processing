from io import BytesIO

import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse


class Visualizer:
    def __init__(self, df):
        self.df = df

    def visualize(self, chart_type, columns):
        buffer = BytesIO()

        if chart_type == "histogram":
            self.df[columns].hist()
        elif chart_type == "scatter" and len(columns)  == 2:
            self.df.plot.scatter(x=columns[0], y=columns[1])
        else:
            raise ValueError("Unsupported chart type or incorrect columns specified")

        plt.savefig(buffer, format="png")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/png")
