/**
 * Dynamic device rows for the energy input form.
 */
(function () {
  const container = document.getElementById("device-rows");
  const addBtn = document.getElementById("add-device-btn");
  const categories = window.NEXERGY_CATEGORIES || ["Other"];
  let rowIndex = 0;

  function categoryOptions(selected) {
    return categories
      .map(function (c) {
        const sel = c === selected ? " selected" : "";
        return '<option value="' + c + '"' + sel + ">" + c + "</option>";
      })
      .join("");
  }

  function createDeviceRow(data) {
    data = data || {};
    const idx = rowIndex++;
    const row = document.createElement("div");
    row.className = "device-row glass-card p-4";
    row.dataset.index = idx;

    row.innerHTML =
      '<button type="button" class="remove-device" aria-label="Remove device">Remove</button>' +
      '<div class="grid md:grid-cols-2 lg:grid-cols-4 gap-3 mt-2">' +
      '<div><label class="form-label">Device Name *</label>' +
      '<input type="text" name="device_name[]" class="nex-input" required value="' +
      (data.name || "") +
      '"></div>' +
      '<div><label class="form-label">Category</label>' +
      '<select name="device_category[]" class="nex-input">' +
      categoryOptions(data.category || "Light") +
      "</select></div>" +
      '<div><label class="form-label">Block</label>' +
      '<input type="text" name="device_block[]" class="nex-input" value="' +
      (data.block || "Main") +
      '"></div>' +
      '<div><label class="form-label">Floor #</label>' +
      '<input type="number" name="device_floor[]" class="nex-input" min="0" value="' +
      (data.floor !== undefined ? data.floor : 1) +
      '"></div>' +
      '<div><label class="form-label">Zone / Dept</label>' +
      '<input type="text" name="device_zone[]" class="nex-input" value="' +
      (data.zone || "General") +
      '"></div>' +
      '<div><label class="form-label">Wattage (W) *</label>' +
      '<input type="number" name="device_wattage[]" class="nex-input" min="1" step="1" required value="' +
      (data.wattage || 100) +
      '"></div>' +
      '<div><label class="form-label">Quantity</label>' +
      '<input type="number" name="device_quantity[]" class="nex-input" min="1" value="' +
      (data.quantity || 1) +
      '"></div>' +
      '<div><label class="form-label">Hours / Day</label>' +
      '<input type="number" name="device_hours[]" class="nex-input" min="0" max="24" step="0.5" value="' +
      (data.hours || 8) +
      '"></div>' +
      '<div><label class="form-label">Days / Month</label>' +
      '<input type="number" name="device_days[]" class="nex-input" min="1" max="31" value="' +
      (data.days || 30) +
      '"></div>' +
      '<div><label class="form-label">Power Factor</label>' +
      '<input type="number" name="device_pf[]" class="nex-input" min="0.1" max="1" step="0.01" value="' +
      (data.pf || 1) +
      '"></div>' +
      '<div><label class="form-label">Standby (W)</label>' +
      '<input type="number" name="device_standby[]" class="nex-input" min="0" value="' +
      (data.standby || 0) +
      '"></div>' +
      '<div><label class="form-label">Efficiency (0-1)</label>' +
      '<input type="number" name="device_efficiency[]" class="nex-input" min="0.1" max="1" step="0.01" value="' +
      (data.efficiency || 1) +
      '"></div>' +
      '<div class="flex items-end gap-2 pb-1">' +
      '<label class="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">' +
      '<input type="checkbox" name="device_critical_' +
      idx +
      '" class="rounded border-neon/50"' +
      (data.critical ? " checked" : "") +
      "> Critical load</label></div></div>";

    row.querySelector(".remove-device").addEventListener("click", function () {
      if (container.children.length > 1) {
        row.remove();
      } else {
        alert("Keep at least one device row.");
      }
    });

    container.appendChild(row);
  }

  addBtn.addEventListener("click", function () {
    createDeviceRow();
  });

  // Default starter row
  createDeviceRow({
    name: "LED Panel",
    category: "Light",
    wattage: 40,
    quantity: 50,
    hours: 12,
  });
})();
