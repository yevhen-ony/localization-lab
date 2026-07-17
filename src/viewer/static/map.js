const emitterId = "drone-1";
const map = document.getElementById("drone-map");


var track = {
    name: "Track",
    x: [],
    y: [],
    mode: "markers",
    type: "scatter",
    marker: {
        size: 1,
        opacity: 0,
    },
    hoverinfo: "skip",
    showlegend: false,
}

var truth = {
    name: "Truth",
    x: [],
    y: [],
    mode: "markers",
    type: "scatter",
    marker: { size: 2, color: "black" }
}

var local = {
    name: "Local",
    x: [],
    y: [],
    mode: "markers",
    type: "scatter",
    marker: {
        size: 1,
        opacity: 0,
    },
    hoverinfo: "skip",
    showlegend: false,
}


var layout = {
    title: "Drone Position",
    xaxis: {
        title: "X, m",
        zeroline: true,
        scaleanchor: "y",
        scaleratio: 1,
    },
    yaxis: {
        title: "Y, m",
        zeroline: true,
    },
    shapes: [], 
    margin: { t: 48, r: 24, b: 56, l: 64 },
}

var config = { responsive: true }

Plotly.newPlot(map, [track, local, truth], layout, config);

const trackWS = new WebSocket(`ws://${window.location.host}/ws/tracks/${emitterId}`);
trackWS.onclose = () => {
    console.log("track websocket closed");
};

const truthWS = new WebSocket(`ws://${window.location.host}/ws/truth/${emitterId}`);
truthWS.onclose = () => {
    console.log("truth websocket closed");
};

const localWS = new WebSocket(`ws://${window.location.host}/ws/local/${emitterId}`);
localWS.onclose = () => {
    console.log("local websocket closed");
};


const trackCircles = []
const localCircles = []


trackWS.onmessage = (event) => {
    const samples = JSON.parse(event.data);
    for (const sample of samples) {
        trackCircles.push(toCircle(sample, "220, 40, 40"))
    }
};

localWS.onmessage = (event) => {
    const samples = JSON.parse(event.data);
    for (const sample of samples) {
        localCircles.push(toCircle(sample, "130, 130, 130"))
    }
};

truthWS.onmessage = (event) => {
    const samples = JSON.parse(event.data);

    for (const sample of samples) {
        Plotly.extendTraces("drone-map", {
            x: [[sample.position.x]],
            y: [[sample.position.y]],
        }, [2]);
    }
    renderCircles()
};


function toCircle(sample, color) {
    const radius = sample.position_std;
    const x = sample.position.x;
    const y = sample.position.y;

    return {
        type: "circle",
        xref: "x",
        yref: "y",
        layer: "above",
        x0: x - radius,
        x1: x + radius,
        y0: y - radius,
        y1: y + radius,
        line: {
            color: `rgba(${color}, 1)`,
            width: 2,
        },
        fillcolor: `rgba(${color}, 0.2)`,
    };
}

function renderCircles() {
    Plotly.relayout(map, {
        shapes: [...trackCircles, ...localCircles],
    });
}
