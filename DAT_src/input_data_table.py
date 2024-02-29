#%%
from dash import Dash, dcc, html, Input, Output, dash_table, no_update
import pandas as pd
import json
from copy import copy

from kobo_api_access import load_kobo_data

# Load survey data from Kobo and get only dict (position 0)
#survey_data = load_kobo_data("aTXghtq4jKcREbYm6Sr8bX")[0]

test_data = [
    {
        'id': 123,
        'name': 'low_income_hh',
        'num': 30,
        'appliances':
            {
                'indoor_lights': {
                    'number': 4,
                    'power': 6,
                    'usage_time': 2,
                    'usage_window': 'window_1, window_2, window_3'
                },
                'Fan': {
                    'number': 1,
                    'power': 15,
                    'usage_time': 1,
                    'usage_window': 'window_1, window_2, window_3'
                }
            }
    },
    {
        'id': 23,
        'name': 'medium_income_hh',
        'num': 5,
        'appliances':
            {
                'indoor_lights': {
                    'number': 4,
                    'power': 6,
                    'usage_time': 2,
                    'usage_window': 'window_1, window_2, window_3'
                },
                'TV': {
                    'number': 1,
                    'power': 50,
                    'usage_time': 1,
                    'usage_window': 'window_1, window_2, window_3'
                }
            }
    }
]


#%% Prepare table for dash

# Check if table data contains sub-data to be displayed in secondary table
sub_data_dict = {}
for row in test_data:  # loop through every row of table (=every survey response)
    for key, value in row.items():  # loop through dict containing this row's data
        # Check if value is dict
        if isinstance(value, dict):  # then this cell contains sub-data
            # Add this cells data to sub_data_dict
            sub_data_dict[(row['id'], key)] = copy(value)

            # -- Replace this rows value with string
            new_cell_string = ""
            for name in value:
                new_cell_string = new_cell_string + name + ", "
            new_cell_string = new_cell_string[:-2]  # Cut last comma and space
            row[key] = copy(new_cell_string)  # replace cell value with string

# Prepare sub-data dict to display in dash
for key, entry in sub_data_dict.items():
    # Turn dict entries into dataframes
    sub_data_dict[key] = pd.DataFrame(entry).T
    # Make index column -> to make sure it's displayed in dash table
    sub_data_dict[key].insert(loc=0, column='name', value=sub_data_dict[key].index)

# turn test_data into dataframe
df = pd.DataFrame(test_data)
#%%
if (10, 'appliances') in sub_data_dict:
    print('yes')
else:
    print('no')

#%%
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

initial_active_cell = {"row": 0, "column": 0, "column_id": "country", "row_id": 0}

app.layout = html.Div(
    [
        html.Div(
            [
                html.H3("Survey responses", style={"textAlign": "center"}),
                dash_table.DataTable(
                    id="table",
                    columns=[{"name": c, "id": c} for c in df.columns],
                    data=df.to_dict("records"),
                    page_size=10,
                    sort_action="native",
                    active_cell=initial_active_cell,
                ),
            ],
            style={"margin": 50},
            className="row"
        ),

        html.Div(id="details", className="row"),
    ],
    className="row")

@app.callback(
    Output("details", "children"), Input("table", "active_cell"),
)
def cell_clicked(active_cell):
    if active_cell is None:
        return no_update

    print(active_cell)
    row_id = active_cell["row_id"]
    print(f"row id: {row_id}")

    col_id = active_cell["column_id"]
    print(f"column id: {col_id}")
    print("---------------------")


    # Check if active cell has sub-data (=entry exists in sub-data dict)
    if (row_id, col_id) in sub_data_dict:
        print('yeees')
        # Get the sub data
        sub_data = sub_data_dict[(row_id, col_id)]
        # Create table of appliances
        sub_data_table = html.Div(
            [dash_table.DataTable(
                id="sub_data_table",
                columns=[{"name": c, "id": c} for c in sub_data.columns],
                data=sub_data.to_dict("records"),
                page_size=10,
                sort_action="native",
                editable=True
            )],
            style={"margin":50}
        )
        return sub_data_table
    else:
        print('no')
        return no_update



app.run_server(debug=True, port=8052)
print('done')



