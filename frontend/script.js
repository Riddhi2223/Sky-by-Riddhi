const API_BASE = "http://127.0.0.1:8000/weather";

async function getWeather() {
    const city = document.getElementById("cityInput").value;
    const errorDiv = document.getElementById("errorMessage");
    errorDiv.innerText = "";

    if (!city) {
        errorDiv.innerText = "Please enter a city name.";
        return;
    }

    try {
        // Current weather
        const response = await fetch(`${API_BASE}/?city=${city}`, {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Error fetching weather.");
        }

        displayCurrentWeather(data);
        loadHistory();

        // Forecast
        const forecastResponse = await fetch(`${API_BASE}/forecast?city=${city}`);
        const forecastData = await forecastResponse.json();

        displayForecast(forecastData);

    } catch (error) {
        errorDiv.innerText = error.message;
    }
}

function displayCurrentWeather(data) {
    const container = document.getElementById("currentWeather");
    const cityName = data.city || data.location;

    container.innerHTML = `
        <div class="weather-main">
            <div class="weather-icon-wrap">
                <img src="https://openweathermap.org/img/wn/${data.icon}@2x.png" alt="${data.description}" />
            </div>
            <div>
                <div class="weather-city">${cityName}</div>
                <div class="weather-temp">${data.temperature}<sup>°C</sup></div>
            </div>
        </div>
        <div class="weather-meta">
            <div class="meta-pill">
                <div class="label">Condition</div>
                <div class="value" style="text-transform: capitalize">${data.description}</div>
            </div>
            <div class="meta-pill">
                <div class="label">Travel Advice</div>
                <div class="value">${data.travel_advice}</div>
            </div>
        </div>
    `;
}

function displayForecast(forecast) {
    const container = document.getElementById("forecastContainer");
    container.innerHTML = "";

    forecast.forEach((day, i) => {
        const div = document.createElement("div");
        div.className = "forecast-item";
        div.style.animationDelay = `${i * 0.07}s`;
        div.innerHTML = `
            <div class="f-date">${day.date.split(" ")[0]}</div>
            <img src="https://openweathermap.org/img/wn/${day.icon}.png" alt="${day.description}" />
            <div class="f-temp">${day.temperature}°</div>
            <div class="f-desc">${day.description}</div>
        `;
        container.appendChild(div);
    });
}

function getLocationWeather() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            try {
                const response = await fetch(
                    `${API_BASE}/?lat=${lat}&lon=${lon}`,
                    { method: "POST" }
                );

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail || "Location weather error.");
                }

                displayCurrentWeather(data);
                loadHistory();

            } catch (error) {
                document.getElementById("errorMessage").innerText = error.message;
            }
        });
    } else {
        alert("Geolocation not supported.");
    }
}

async function loadHistory() {
    const response = await fetch(`${API_BASE}/history`);
    const data = await response.json();

    const container = document.getElementById("historyContainer");
    container.innerHTML = "";

    data.forEach((item, i) => {
        const div = document.createElement("div");
        div.className = "history-item";
        div.style.animationDelay = `${i * 0.05}s`;
        div.innerHTML = `
            <div>
                <span class="h-city">${item.city}</span>
                <span class="h-temp">${item.temperature}°C</span>
                <div class="h-desc">${item.description}</div>
            </div>
            <div class="history-actions">
                <button class="btn-icon btn-edit" onclick="updateRecord(${item.id})">✎ Edit</button>
                <button class="btn-icon btn-delete" onclick="deleteRecord(${item.id})">✕ Delete</button>
            </div>
        `;
        container.appendChild(div);
    });
}

async function deleteRecord(id) {
    await fetch(`${API_BASE}/history/${id}`, {
        method: "DELETE"
    });
    loadHistory();
}

async function updateRecord(id) {
    const newCity = prompt("Enter new city:");
    if (!newCity) return;

    await fetch(`${API_BASE}/history/${id}?new_city=${newCity}`, {
        method: "PUT"
    });
    loadHistory();
}

function exportCSV() {
    window.open(`${API_BASE}/export/csv`);
}

// Allow pressing Enter to search
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("cityInput");
    if (input) {
        input.addEventListener("keydown", e => {
            if (e.key === "Enter") getWeather();
        });
    }
});

window.onload = loadHistory;
