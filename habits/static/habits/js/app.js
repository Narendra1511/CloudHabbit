document.addEventListener('DOMContentLoaded', function () {
  const chartEl = document.getElementById('habitChart');
  if (!chartEl) return;

  const labels = chartEl.dataset.labels ? chartEl.dataset.labels.replace(/&#x27;/g, '"') : '[]';
  const values = chartEl.dataset.values || '[]';

  let parsedLabels = [];
  let parsedValues = [];
  try {
    parsedLabels = JSON.parse(labels);
    parsedValues = JSON.parse(values);
  } catch (e) {
    console.warn('Chart data could not be parsed.', e);
  }

  new Chart(chartEl, {
    type: 'bar',
    data: {
      labels: parsedLabels,
      datasets: [{
        label: 'Completed logs',
        data: parsedValues,
        borderWidth: 1,
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { color: '#d9e8fb' }, grid: { color: 'rgba(255,255,255,.08)' } },
        x: { ticks: { color: '#d9e8fb' }, grid: { color: 'rgba(255,255,255,.04)' } }
      }
    }
  });
});
