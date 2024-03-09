import gborns from "../gborns.js";
const byYear = gborns.reduce((acc, state) => {
  if (acc[state.id_year]) {
    acc[state.id_year].push(state);
  } else {
    acc[state.id_year] = [state];
  }

  return acc;
}, {});

// Get years from byYear
const years = Object.keys(byYear);

fetch("https://unpkg.com/us-atlas/states-10m.json")
  .then((r) => r.json())
  .then((us) => {
    const nation = ChartGeo.topojson.feature(us, us.objects.nation).features[0];
    const states = ChartGeo.topojson.feature(us, us.objects.states).features;
    const chart = new Chart(document.getElementById("chart").getContext("2d"), {
      type: "choropleth",
      data: {
        labels: states.map((d) => d.properties.name),
        datasets: [
          {
            label: "States",
            outline: nation,
            data: [],
          },
        ],
      },
      options: {
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          projection: {
            axis: "x",
            projection: "albersUsa",
          },
          color: {
            axis: "x",
            quantize: 5,
            legend: {
              position: "bottom-right",
              align: "bottom",
            },
          },
        },
      },
    });
    // Create buttons for each year and add event listeners
    const buttonContainer = document.getElementById("button-container");
    years.sort((a, b) => b - a);
    let firstButton;
    years.forEach((year, index) => {
      const button = document.createElement("button");
      button.innerText = year;
      buttonContainer.appendChild(button);
      // Add event listener to update the chart data when the button is clicked
      button.addEventListener("click", () => {
        // Update the chart data with the new year data
        const newData = states.map((d) => ({
          feature: d,
          value: byYear[year].find((val) => d.properties.name == val.state)
            ?.population,
        }));
        // Update the chart data and update the chart to show the new data
        chart.data.datasets[0].data = newData;
        chart.update();
      });
      // Save the first button to trigger a click
      if (index === 0) {
        firstButton = button;
      }
    });
    // Trigger the first button click to show the first year
    if (firstButton) {
      firstButton.click();
    }
  });
