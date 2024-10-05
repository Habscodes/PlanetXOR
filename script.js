let weather = {
  apiKey: "de8380bb4a4ac3e4f0017115ff3b84a6", // OpenWeather API key
  nasaApiKey: "pxnpO5BUN4IBrotreGT6ZDBCmxgyIelzEduk5dEq", // Your NASA API key

  // Fetch weather from OpenWeather API
  fetchWeather: function (city) {
    fetch(
      "https://api.openweathermap.org/data/2.5/weather?q=" +
        city +
        "&units=metric&appid=" +
        this.apiKey
    )
      .then((response) => {
        if (!response.ok) {
          this.displayError();
          throw new Error("No weather found.");
        }
        return response.json();
      })
      .then((data) => {
        this.displayWeather(data);
        this.fetchGreenhouseData(); // Fetch greenhouse gas data here
      })
      .catch((error) => console.log(error));
  },

  // Fetch greenhouse gas data from NASA API
  fetchGreenhouseData: function () {
    fetch(`https://api.nasa.gov/ghg/endpoint?api_key=${this.nasaApiKey}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("No greenhouse data found.");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data); // Log the response data
        this.displayGreenhouseData(data); // Call function to display data
      })
      .catch((error) => console.log(error));
  },
  
  // Display weather data
  displayWeather: function (data) {
    const { name } = data;
    const { icon, description } = data.weather[0];
    const { temp, humidity } = data.main;
    const { speed } = data.wind;

    // Update the DOM with weather data
    document.querySelector(".city").innerText = "Weather in " + name;
    document.querySelector(".icon").src =
      "https://openweathermap.org/img/wn/" + icon + ".png";
    document.querySelector(".description").innerText = description;
    document.querySelector(".temp").innerText = temp + "°C";
    document.querySelector(".humidity").innerText =
      "Humidity: " + humidity + "%";
    document.querySelector(".wind").innerText =
      "Wind speed: " + speed + " km/h";

    // Remove loading class once data is displayed
    document.querySelector(".weather").classList.remove("loading");
  },
  
  displayGreenhouseData: function (data) {
    const co2Levels = data.co2 || "No CO2 data available"; // Replace with actual property names
    const methaneLevels = data.methane || "No Methane data available"; // Example for methane
  
    document.querySelector(".greenhouse-info").innerText = 
      `CO2 Levels: ${co2Levels} ppm\nMethane Levels: ${methaneLevels} ppm`;
  },
  
  

  // Set the custom background image from Unsplash
  setCustomBackground: function () {
    document.body.style.backgroundImage =
      "url('ft-shafi-1OReA9hJN5A-unsplash.jpg')";
    document.body.style.backgroundSize = "cover";
    document.body.style.backgroundPosition = "center";
  },

  // Display error if no city found
  displayError: function () {
    document.querySelector(".city").innerText = "City not found";
    document.querySelector(".icon").src = "";
    document.querySelector(".description").innerText = "";
    document.querySelector(".temp").innerText = "";
    document.querySelector(".humidity").innerText = "";
    document.querySelector(".wind").innerText = "";
  },

  // Search for weather based on input
  search: function () {
    this.fetchWeather(document.querySelector(".search-bar").value);
  },
};

// Event listeners for search button and Enter key press
document.querySelector(".search button").addEventListener("click", function () {
  weather.search();
});

document
  .querySelector(".search-bar")
  .addEventListener("keyup", function (event) {
    if (event.key == "Enter") {
      weather.search();
    }
  });

// Set the initial background on page load
weather.setCustomBackground(); // Call this method here

// Fetch default weather on page load
weather.fetchWeather("Lagos");
