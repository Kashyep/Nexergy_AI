/**
 * Chart.js charts for the energy dashboard.
 */
(function () {
  const el = document.getElementById("chart-data");
  if (!el || typeof Chart === "undefined") return;

  const data = JSON.parse(el.textContent);
  const neon = "#00FF9C";
  const neonAlt = "#39FF14";
  const gridColor = "rgba(255,255,255,0.08)";

  const defaultOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#9ca3af" },
      },
    },
    scales: {
      x: {
        ticks: { color: "#9ca3af" },
        grid: { color: gridColor },
      },
      y: {
        ticks: { color: "#9ca3af" },
        grid: { color: gridColor },
      },
    },
  };

  function labelsFrom(arr) {
    return arr.map(function (x) {
      return x.label;
    });
  }

  function valuesFrom(arr) {
    return arr.map(function (x) {
      return x.kwh;
    });
  }

  // Device bar chart
  if (data.by_device && data.by_device.length) {
    new Chart(document.getElementById("chartDevices"), {
      type: "bar",
      data: {
        labels: labelsFrom(data.by_device),
        datasets: [
          {
            label: "kWh / month",
            data: valuesFrom(data.by_device),
            backgroundColor: "rgba(0, 255, 156, 0.5)",
            borderColor: neon,
            borderWidth: 1,
          },
        ],
      },
      options: defaultOptions,
    });
  }

  // Category doughnut
  if (data.by_category && data.by_category.length) {
    new Chart(document.getElementById("chartCategories"), {
      type: "doughnut",
      data: {
        labels: labelsFrom(data.by_category),
        datasets: [
          {
            data: valuesFrom(data.by_category),
            backgroundColor: [
              "#00FF9C",
              "#00E676",
              "#39FF14",
              "#07110B",
              "rgba(0,255,156,0.4)",
              "rgba(57,255,20,0.5)",
            ],
            borderColor: "#050505",
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "right", labels: { color: "#9ca3af" } },
        },
      },
    });
  }

  // Block bar chart
  if (data.by_block && data.by_block.length) {
    new Chart(document.getElementById("chartBlocks"), {
      type: "bar",
      data: {
        labels: labelsFrom(data.by_block),
        datasets: [
          {
            label: "kWh by block",
            data: valuesFrom(data.by_block),
            backgroundColor: "rgba(57, 255, 20, 0.45)",
            borderColor: neonAlt,
          },
        ],
      },
      options: { ...defaultOptions, indexAxis: "y" },
    });
  }

  // Solar bill comparison on dashboard
  if (data.solar_bills) {
    new Chart(document.getElementById("chartSolarBill"), {
      type: "bar",
      data: {
        labels: data.solar_bills.labels,
        datasets: [
          {
            label: "₹ / month",
            data: data.solar_bills.values,
            backgroundColor: ["rgba(248,113,113,0.5)", "rgba(0,255,156,0.55)"],
            borderColor: ["#f87171", neon],
            borderWidth: 1,
          },
        ],
      },
      options: defaultOptions,
    });
  }
})();
