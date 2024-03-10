import gborns from "../gborns.js";

const byYear = gborns.reduce((acc, state) => {
  if (acc[state.id_year]) {
    acc[state.id_year].push(state);
  } else {
    acc[state.id_year] = [state];
  }

  return acc;
}, {});

// Get Years from byYear
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
            axis: 'x',
            quantize: 20,
            legend: {
              position: 'bottom-right',
              align: 'right',
            },
          },
        },
      },
    });
    // Create buttons for each year and add event listeners
    const buttonContainer = document.getElementById("button-container");
    const chartContainer = document.getElementById("chart");
    chartContainer.classList.add(
      "transition-opacity",
      "duration-500",
      "ease-in-out",
      "opacity-100"
    );
    years.sort((a, b) => b - a);
    let firstButton;
    years.forEach((year, index) => {
      const button = document.createElement("button");
      button.className =
        "font-bold border-2 border-gray-500 bg-white text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-700 focus:ring-opacity-50";
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
        chartContainer.classList.remove("opacity-100");
        chartContainer.classList.add("opacity-0");
        // Update the chart data and update the chart to show the new data after a short delay to allow the chart to fade out
        setTimeout(() => {
          // Update the chart data and update the chart to show the new data after a short delay to allow the chart to fade out
          chart.data.datasets[0].data = newData;
          chart.update();
          chartContainer.classList.remove("opacity-0");
          chartContainer.classList.add("opacity-100");
        }, 500);
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
