import requests
import plotly.graph_objects as go
from datetime import datetime

def GraphPatientReaction(reaction="fatigue", start="20200101", end="20201231"):
    text = (f"https://api.fda.gov/drug/event.json?search=(receivedate:[{start}+TO+{end}])+AND+patient.reaction.reactionmeddrapt:{reaction}&count=receivedate")
    response = requests.get(text)

    if response.status_code == 200:
        data = response.json()
        results = data["results"]
        if results:
            # Extract time and count data
            time = []
            count = []
            for result in results:
                time.append(result["time"])
                count.append(result["count"])

            # Convert time to a datetime object
            time = [datetime.strptime(date, "%Y%m%d") for date in time]

            # Create a trendline graph
            fig = go.Figure(data=go.Scatter(x=time, y=count))
            fig.update_layout(
              xaxis_title="Time",
              yaxis_title="Count",
              title=f"Adverse Reaction Trendline: {reaction} between {start} to {end}"
            )
            fig.write_html("fig.html")
        else:
          print("No adverse reaction reports found.")
    else:
        print(f"An error occurred: {response.status_code}")
