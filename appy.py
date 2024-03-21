import plotly.express as px
from shiny.express import input, ui, render
from shiny import render, reactive
from shinywidgets import render_plotly
import palmerpenguins
import seaborn as sns

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Suarez Penguin Data", fillable=True)

with ui.sidebar(open="open"):
    ui.h2("Sidebar")

    ui.input_selectize(
        "selected_attribute",
        "Select Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    ui.input_numeric("Plotly_bin_count", "Bin Count", 1, min=1, max=50)

    ui.input_slider("seaborn_bin_count", "Seaborn Slider", 0, 100, 50)

    ui.input_checkbox_group(
        "Selected_Species_list",
        "Species Checkbox",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )

    ui.hr()

    ui.a(
        "Github",
        href="https://github.com/edgarsuarez9/cintel-02-data/tree/main",
        target="_blank",
    )

with ui.layout_columns():
    with ui.card(full_screen=True):

        ui.h4("Palmer Penguins Data Table")

        @render.data_frame
        def penguins_datatable():
            return render.DataTable(filtered_data())

    with ui.card(full_screen=True):

        ui.h4("Palmer Penguins Data Grid")

        @render.data_frame
        def penguins_data():
            return render.DataGrid(filtered_data())

with ui.layout_columns(col_widths=(20, 80)):
    with ui.card(full_screen=True):
        ui.h4("Species Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(filtered_data(), x="species", color="species")

with ui.accordion():
    with ui.accordion_panel(title="Seaborn Histogram", full_screen=True):
        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
            bins = input.seaborn_bin_count()
            ax = sns.histplot(data=filtered_data(), x="body_mass_g", bins=bins, hue="species")
            ax.set_title("Palmer Penguins")
            ax.set_xlabel("Mass")
            ax.set_ylabel("Count")
            return ax

    with ui.accordion_panel(title="Plotly Scatter Plot", full_screen=True):
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                title="Plotly Scatter Plot",
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                labels={
                    "bill_length_mm": "Bill Length (mm)",
                    "body_mass_g": "Body Mass (g)",
                },
            )

@reactive.calc
def filtered_data():
    return penguins_df
