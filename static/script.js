
    let latencyData = [];
    let labels = [];

    const ctx = document.getElementById('latencyChart').getContext('2d');
    const latencyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Latency (ms)',
                data: latencyData,
                tension: 0.3
            }]
        }
    });



async function loadStatus() {
    const res = await fetch("http://127.0.0.1:8000/status");
    const devices = await res.json();

    const container = document.getElementById("device-container");
    container.innerHTML = "";

    const now = new Date().toLocaleTimeString();

    devices.forEach(d => {
        console.log("DEVICE OBJECT:", d);
        const div = document.createElement("div");
        div.className = "device-card";
        div.innerHTML = `
            <span>
                ${d.name} (${d.ip})<br>
                <small>Latency: ${d.latency ?? "N/A"} ms</small>
            </span>
            <span class="status ${d.status.toLowerCase()}">${d.status}</span>
        `;
        container.appendChild(div);

    if (d.status === "UP") {
        labels.push(new Date().toLocaleTimeString());
    latencyData.push(Math.floor(Math.random() * 100) + 10);
    latencyChart.update();
    }


/*
        // Add latency to graph (only if UP)
    if (d.latency !== null) {
        labels.push(new Date().toLocaleTimeString());
        latencyData.push(Number(d.latency));

        if (latencyData.length > 10) {
            latencyData.shift();
            labels.shift();
        }

        latencyChart.update();
    }
*/


    });
}

loadStatus();
setInterval(loadStatus, 3000); // every 3 seconds

