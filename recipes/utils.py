from .models import Recipe
from io import BytesIO
import base64
import matplotlib.pyplot as plt


# define a function that takes the ID
def get_recipename_from_id(val):
    recipename = Recipe.objects.get(id=val)
    # and the name is returned back
    return recipename


def get_graph():
    # create a BytesIO buffer for the image
    buffer = BytesIO()

    # create a plot with a bytesIO object as a file-like object. Set format to png
    plt.savefig(buffer, format="png")

    # set cursor to the beginning of the stream
    buffer.seek(0)

    # retrieve the content of the file
    image_png = buffer.getvalue()

    # encode the bytes-like object
    graph = base64.b64encode(image_png)

    # decode to get the string as output
    graph = graph.decode("utf-8")

    # free up the memory of buffer
    buffer.close()

    # return the image/graph
    return graph


# chart_type: user input o type of chart,
# data: pandas dataframe


def get_chart(chart_type, data, **kwargs):
    plt.switch_backend("AGG")

    fig = plt.figure(figsize=(11.5, 6))

    # select chart_type based on user input from the form
    if chart_type == "#1":
        plt.bar(data["name"], data["cooking_time"])
        plt.xlabel(
            "Recipe Name(s)", fontsize=15, fontweight="bold"
        )  # Change font size of x-label
        plt.ylabel(
            "Cooking Time", fontsize=15, fontweight="bold"
        )  # Change font size of y-label
        plt.xticks(rotation=70)

    elif chart_type == "#2":
        labels = kwargs.get("labels")
        # Customize pie chart size of labels
        plt.pie(
            data["cooking_time"],
            labels=labels,
            labeldistance=1.1,
            textprops={"fontsize": 8},
        )
        # Add label at the bottom
        plt.xlabel(
            "Recipe Name(s)", fontsize=15, fontweight="bold"
        )  # Change font size of x-label

    elif chart_type == "#3":
        plt.plot(data["name"], data["cooking_time"])
        plt.xlabel("Recipe Name(s)", fontsize=15, fontweight="bold")
        plt.ylabel("Cooking Time", fontsize=15, fontweight="bold")
        plt.xticks(rotation=70)

    else:
        print("unknown chart type")

    # specify layout details
    plt.tight_layout()

    # render the graph to file
    chart = get_graph()
    return chart
