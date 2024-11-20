const cal = new CalHeatmap();
cal.paint({
  itemSelector: "#mood-count-heatmap",
  data: {
    source:
      "/mood/statistics/heatmap/?start={{start=YYYY-MM-DD}}&end={{end=YYYY-MM-DD}}",
    x: "date",
    y: "value",
  },
  date: {
    start: new Date(new Date().setFullYear(new Date().getFullYear() - 1)), // Start from one year ago
  },
  range: 13, // Display 13 months so that the current month is included
  domain: {
    type: "month",
    label: {
      position: "top",
      text: "MMM YYYY",
    },
  },
  subDomain: {
    type: "ghDay",
    width: 10,
    height: 10,
  },
  highlight: [new Date()],
});
