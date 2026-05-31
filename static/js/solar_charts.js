/**
 * Solar before/after bill chart.
 */
(function () {
  const el = document.getElementById("solar-chart-data");
  if (!el || typeof Chart === "undefined") return;

  const data = JSON.parse(el.textContent);
  const ctx = document.getElementById("chartSolar");
  if (!ctx) return;

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [
        {
          label: "Monthly Bill (₹)",
          data: data.bills,
          backgroundColor: ["rgba(248, 113, 113, 0.55)", "rgba(0, 255, 156, 0.55)"],
          borderColor: ["#f87171", "#00FF9C"],
          borderWidth: 2,
          borderRadius: 8,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            afterLabel: function (ctx) {
              if (ctx.dataIndex === 1 && data.generation) {
                return "Solar gen: " + data.generation + " kWh/mo";
              }
              return "";
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { color: "#9ca3af" },
          grid: { color: "rgba(255,255,255,0.08)" },
        },
        x: {
          ticks: { color: "#9ca3af" },
          grid: { display: false },
        },
      },
    },
  });
})();
