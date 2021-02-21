const queryString = window.location.search;

var margin = { top: 30, right: 120, bottom: 30, left: 50 },
width = 960 - margin.left - margin.right,
height = 500 - margin.top - margin.bottom,
tooltip = { width: 100, height: 100, x: 10, y: -30 };

var parseDate = d3.timeParse("%Y-%m-%d %H:%M"),
bisectDate = d3.bisector(function(d) { return d.date; }).left,
formatValue = d3.format(","),
dateFormatter = d3.timeFormat("%d.%m.%y %H:%M");

var x = d3.scaleTime()
    .range([0, width]);

var y = d3.scaleLinear()
    .range([height, 0]);

var valueline = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.value); });

var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

var xAxis = d3.axisBottom(x)
.tickFormat(dateFormatter);

var yAxis = d3.axisLeft(y)
.tickFormat(d3.format("s"))

var line = d3.line()
.x(function(d) { return x(d.date); })
.y(function(d) { return y(d.likes); });

var svg = d3.select("#my_dataviz")
.append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
.append("g")
  .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

    d3.csv("csv/" + queryString).then(function(data) {

        data.forEach(function(d) {
            d.date = parseDate(d.date);
            d.value = d.value;
        });

        data.sort(function(a, b) {
            return a.date - b.date;
        });

        x.domain([data[0].date, data[data.length - 1].date]);
        y.domain(d3.extent(data, function(d) { return d.value; }));

    // add the valueline path.
    svg.append("path")
        .data([data])
        .attr("class", "line")
        .attr("d", valueline);

    // add the dots with tooltips
    svg.selectAll("dot")
        .data(data)
    .enter().append("circle")
        .attr("r", 5)
        .attr("cx", function(d) { return x(d.date); })
        .attr("cy", function(d) { return y(d.value); })
        .on("mouseover", function(event,d) {
        div.transition()
            .duration(200)
            .style("opacity", .9);
        div.html(dateFormatter(d.date) + "<br/>" + d.value)
            .style("left", (event.pageX) + "px")
            .style("top", (event.pageY - 28) + "px");
        })
        .on("mouseout", function(d) {
        div.transition()
            .duration(500)
            .style("opacity", 0);
        });

    // add the X Axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // add the Y Axis
    svg.append("g")
        .call(d3.axisLeft(y));

    });