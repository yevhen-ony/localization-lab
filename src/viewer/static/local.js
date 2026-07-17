const emitterId = "drone-1";
const tbody = document.getElementById("samples");

const ws = new WebSocket(`ws://${window.location.host}/ws/local/${emitterId}`);

ws.onmessage = (event) => {
    const samples = JSON.parse(event.data);

    for (const sample of samples) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${sample.epoch}</td>
            <td>${sample.emitter_id}</td>
            <td>${sample.position.x.toFixed(2)}</td>
            <td>${sample.position.y.toFixed(2)}</td>
            <td>${sample.position_std.toFixed(2)}</td>
        `;

        tbody.prepend(row);
    }
};

ws.onclose = () => {
    console.log("local websocket closed");
};
