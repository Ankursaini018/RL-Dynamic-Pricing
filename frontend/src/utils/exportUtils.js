/**
 * exportUtils.js
 * High quality export utilities for PNG charts and CSV datasets.
 */

// Export SVG chart to PNG image download
export function exportChartAsPNG(svgElementId, filename = "chart-export.png") {
  const svgElement = document.getElementById(svgElementId);
  if (!svgElement) {
    console.error(`SVG element with id "${svgElementId}" not found`);
    return;
  }

  // Clone SVG to avoid altering DOM
  const svgClone = svgElement.cloneNode(true);
  const bbox = svgElement.getBoundingClientRect();
  const width = bbox.width || 800;
  const height = bbox.height || 400;

  svgClone.setAttribute("width", width);
  svgClone.setAttribute("height", height);

  // Inline styling for background
  const svgData = new XMLSerializer().serializeToString(svgClone);
  const canvas = document.createElement("canvas");
  canvas.width = width * 2; // 2x retina scale
  canvas.height = height * 2;
  const ctx = canvas.getContext("2d");

  // Dark background fill
  ctx.fillStyle = "#0d0d1a";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const img = new Image();
  const svgBlob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
  const url = URL.createObjectURL(svgBlob);

  img.onload = () => {
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    URL.revokeObjectURL(url);

    const a = document.createElement("a");
    a.download = filename;
    a.href = canvas.toDataURL("image/png");
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };
  img.src = url;
}

// Export structured array to CSV file download
export function exportDataAsCSV(data, filename = "dataset-export.csv") {
  if (!data || !data.length) {
    console.error("No data available to export to CSV");
    return;
  }

  const headers = Object.keys(data[0]);
  const rows = data.map((obj) =>
    headers
      .map((header) => {
        let val = obj[header];
        if (typeof val === "string" && val.includes(",")) {
          return `"${val}"`;
        }
        return val !== undefined && val !== null ? val : "";
      })
      .join(",")
  );

  const csvContent = [headers.join(","), ...rows].join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
