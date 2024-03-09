import gborns from "../gborns.js";

const byYear = gborns.reduce((acc, state) => {
  if (acc[state.id_year]) {
    acc[state.id_year].push(state)
  } else {
    acc[state.id_year] = [state]
  }
  
  return acc
}, {})

console.log(byYear)

fetch('https://unpkg.com/us-atlas/states-10m.json').then((r) => r.json()).then((us) => {
    const nation = ChartGeo.topojson.feature(us, us.objects.nation).features[0];
    const states = ChartGeo.topojson.feature(us, us.objects.states).features;

    const chart = new Chart(document.getElementById("chart").getContext("2d"), {
        type: 'choropleth',
        data: {
            labels: states.map((d) => d.properties.name),
            datasets: [{
                label: 'States',
                outline: nation,
                data: states.map((d) => ({
                    feature: d,
                    value: byYear['2013'].find(val => d.properties.name == val.state)?.population // hacer match este dato con el state de nuestros datos
                }))
            }]
        },
        options: {
            plugins: {
                legend: {
                  display: false
                },
              },
              scales: {
                projection: {
                  axis: 'x',
                  projection: 'albersUsa'  
                },
                color: {
                  axis: 'x',
                  quantize: 5,
                  legend: {
                    position: 'bottom-right',
                    align: 'bottom'
                  },
                }
              },
        }
    })
})