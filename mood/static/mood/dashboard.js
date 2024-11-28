const cal = new CalHeatmap();

fetch("/mood/statistics/heatmap/values/")
  .then((response) => response.json())
  .then((data) => {
    var moodOptions = data;

    const start = new Date(new Date().setFullYear(new Date().getFullYear() - 1));
    const end = new Date();

    var domain = Object.keys(moodOptions).map((key) => Number(key));
    const range = ["#ffffd4"].concat(domain.map((key) => moodOptions[key]["color"]));
    domain = [-Infinity].concat(domain).concat([Infinity]);

    fetch("/mood/statistics/heatmap/?start=" + start.toISOString().split("T")[0] + "&end=" + end.toISOString().split("T")[0])
      .then((response) => response.json())
      .then((data) => {
        cal.paint({
          itemSelector: "#mood-count-heatmap",
          data: {
            source:
              data,
            x: "date",
            y: d => {
              if (d.average) {
                const key = Object.keys(moodOptions).reduce((a, b) => Math.abs(a - d.average) < Math.abs(b - d.average) ? a : b);
                console.log(key, d.average, moodOptions[key]);
                return Number(key);
              }
              return 0;
            },
          },
          scale: {
            color: {
              domain: domain,
              type: "threshold",
              range: range,
            }
          },
          date: {
            start: start,
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
        },
          [
            [
              Tooltip, {
                enabled: true,
                text: function (timestamp, value, dayjsDate) {
                  const date_str = dayjsDate.format("YYYY-MM-DD");

                  const obj = data.find(o => o["date"] === date_str);

                  if (!obj) {
                    return `${date_str}<br>Mood Count: 0<br>Average Mood: N/A`
                  }

                  const average = obj["average"];

                  if (!average) {
                    return `${date_str}<br>Mood Count: ${obj.count}<br>Average Mood: N/A`
                  }

                  const key = Object.keys(moodOptions).reduce((a, b) => Math.abs(a - average) < Math.abs(b - average) ? a : b);
                  const mood = moodOptions[key];

                  return `${date_str}<br>Mood Count: ${obj.count}<br>Average Mood: ${mood.name}`
                }
              }
            ]
          ]
        );
      });
  });