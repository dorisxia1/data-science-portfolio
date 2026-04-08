<template>
    <div class="chart-wrapper">
      <div id="hierarchy-builder" style="margin: 10px 150px;">
        <label><strong>Choose drill-down order:</strong></label><br />
        <select class="hierarchy-step" id="step-0"></select>
        <select class="hierarchy-step" id="step-1"></select>
        <select class="hierarchy-step" id="step-2"></select>
        <select class="hierarchy-step" id="step-3"></select>
        <select class="hierarchy-step" id="step-4"></select>
        <button id="apply-hierarchy">Apply</button>
        <button id="clear-hierarchy">Clear</button>
      </div>
  
      <div id="button-row">
        <button id="replay-animation">Replay Animation</button>
        <button id="back">← Back</button>
        <select id="sort-select">
          <option value="value-desc">Descending ↓</option>
          <option value="value-asc">Ascending ↑</option>
        </select>
      </div>
      
      <div id="breadcrumb" class="breadcrumb"></div>
      <svg id="chart" width="960" height="600"></svg>
      <div id="tooltip"></div>
      

    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue';
  import * as d3 from 'd3';
  
  const formatAbbreviated = d3.format(".1s");
  const regionOnlyOrder = ["Region"];
  const allDimensions = ["Region", "State", "Race", "Gender", "Age"];
  const defaultOrder = ["State", "Race", "Gender", "Age"];
  const stateNames = {
    AL: "Alabama", AK: "Alaska", AZ: "Arizona", AR: "Arkansas", CA: "California", 
    CO: "Colorado", CT: "Connecticut", DE: "Delaware", FL: "Florida", GA: "Georgia",
    HI: "Hawaii", ID: "Idaho", IL: "Illinois", IN: "Indiana", IA: "Iowa",
    KS: "Kansas", KY: "Kentucky", LA: "Louisiana", ME: "Maine", MD: "Maryland",
    MA: "Massachusetts", MI: "Michigan", MN: "Minnesota", MS: "Mississippi", MO: "Missouri",
    MT: "Montana", NE: "Nebraska", NV: "Nevada", NH: "New Hampshire", NJ: "New Jersey",
    NM: "New Mexico", NY: "New York", NC: "North Carolina", ND: "North Dakota", OH: "Ohio",
    OK: "Oklahoma", OR: "Oregon", PA: "Pennsylvania", RI: "Rhode Island", SC: "South Carolina",
    SD: "South Dakota", TN: "Tennessee", TX: "Texas", UT: "Utah", VT: "Vermont", VA: "Virginia", WA: "Washington",
    WV: "West Virginia", WI: "Wisconsin", WY: "Wyoming", DC: "District of Columbia" };
  const regionColors = {
    "West": "#4682B4",
    "South": "#396b90",
    "Midwest": "#4682B4",
    "Northeast": "#4682B4"
  };

  onMounted(async () => {
    const margin = { top: 30, right: 30, bottom: 0, left: 150 };
    const barStep = 27;
    const barPadding = 3 / barStep;
    const width = 960;
    const duration = 750;

    let height = 600;
    let currentSortOption = "value-desc";
    let navigationPath = [];
    let firstRender = true;
  
    const svg = d3.select("#chart");
    const tooltip = d3.select("#tooltip")
      .style("position", "absolute")
      .style("opacity", 0)
      .style("pointer-events", "none")
      .style("background", "#fff")
      .style("border", "1px solid #ccc")
      .style("padding", "6px 10px")
      .style("font-size", "13px")
      .style("border-radius", "4px")
      .style("box-shadow", "0 2px 6px rgba(0,0,0,0.15)");
  
    const x = d3.scaleLinear().range([margin.left, width - margin.right]);
    //const color = d3.scaleOrdinal([true, false], ["steelblue", "#aaa"]);
    
    let flatData = [], root;
  
    function buildHierarchy(data, keys) {
      const root = { name: "", children: [] };

      function nest(data, depth) {
        if (depth >= keys.length) return [];
        const key = keys[depth];
        const grouped = d3.group(data, d => d[key]);

        return Array.from(grouped, ([name, values]) => {
          let node;
          if (depth < keys.length - 1) {
            const sample = values[0]; // sample row
            node = { name };
            if (key === "State" && sample.Region) {
              node.Region = sample.Region;
            }
            node.children = nest(values, depth + 1);
            node.value = d3.sum(node.children, d => d.value);
          } else {
            const leaf = values[0];
            node = {
              name,
              State: leaf.State,
              Region: leaf.Region,
              Race: leaf.Race,
              Gender: leaf.Gender,
              Age: leaf.Age,
              Count: leaf.Count
            };
 
            node.value = d3.sum(values, d => d.Count);
          }
          return node;
        });
      }

      root.children = nest(data, 0);
      root.value = d3.sum(root.children, d => d.value);
      return d3.hierarchy(root).sum(d => d.value).sort((a, b) => b.value - a.value);
    }
  
    function applySort(data, option) {
      if (option === "value-desc") {
        data.children.sort((a, b) => b.value - a.value);
      } else if (option === "value-asc") {
        data.children.sort((a, b) => a.value - b.value);
      // } else if (option === "age-sort") {
      //   data.children.sort((a, b) => ageOrder.indexOf(a.data.name) - ageOrder.indexOf(b.data.name));
      }
    }
  
    function render(d) {
        height = Math.max(600, margin.top + margin.bottom + barStep * d.children.length);
        svg.attr("height", height);
        svg.selectAll("g").remove();

        svg.append("g")
            .attr("class", "x-axis")
            .attr("transform", `translate(0,${margin.top})`)
            .call(d3.axisTop(x).tickFormat(formatAbbreviated));

        svg.append("g")
            .attr("class", "y-axis")
            .attr("transform", `translate(${margin.left + 0.5},0)`)
            .call(g => g.append("line")
            .attr("stroke", "currentColor")
            .attr("y1", margin.top)
            .attr("y2", height));

        const g = svg.append("g")
            .attr("transform", `translate(0,${margin.top + barStep * barPadding})`);

        x.domain([0, d3.max(d.children, d => d.value)]);
       
        const xAxis = d3.axisTop(x).ticks(5).tickFormat(formatAbbreviated);
        
        svg.select(".x-axis")
          .transition()
          .duration(duration)
          .call(xAxis);

        const bars = g.selectAll("g")
            .data(d.children, d => d.data.name)
            .join(
            enter => {
                const bar = enter.append("g")
                .attr("transform", (d, i) => `translate(0,${barStep * i})`)
                .attr("opacity", 0);

                bar.append("text")
                .attr("class", "label-text")
                .attr("x", margin.left - 6)
                .attr("y", barStep * (1 - barPadding) / 2)
                .attr("dy", ".35em")
                .attr("text-anchor", "end")
                .text(d => stateNames[d.data.name] || d.data.name);

                bar.append("rect")
                  .attr("x", x(0))
                  .attr("width", firstRender ? 0 : d => x(d.value) - x(0))
                  .attr("height", barStep * (1 - barPadding))
                  .attr("fill", d => {
                    if (d.depth === 1 && d.data.Region) {
                      // Top level: State → color by region
                      return regionColors[d.data.Region] || "#888";
                    } else if (d.height > 0) {
                      // Intermediate levels (e.g. Race, Gender): still drillable
                      return "#4682B4"; // steelblue
                    } else {
                      // Bottom level (leaf): no children
                      return "#ccc"; // gray
                    }
                  })

                  .on("mouseover", (event, d) => {
                    const label = stateNames[d.data.name] || d.data.name;
                    tooltip.transition().duration(200).style("opacity", 0.95);
                    tooltip.html(`<strong>${label}</strong><br>Count: ${d.value.toLocaleString()}`)
                      .style("left", `${event.pageX + 10}px`)
                      .style("top", `${event.pageY - 28}px`);
                  })
                  .on("mousemove", event => {
                    tooltip.style("left", `${event.pageX + 10}px`)
                      .style("top", `${event.pageY - 28}px`);
                  })
                  .on("mouseout", () => tooltip.transition().duration(200).style("opacity", 0))
                  .on("click", (event, d) => {
                    if (!d.children) return;
                    onDrillDown(d);
                  })

                  .transition()
                  .delay((d, i) => firstRender ? i * 30 : 0)
                  .duration(firstRender ? 700 : 0)
                  .attr("width", d => x(d.value) - x(0));

                return bar.transition().duration(750).attr("opacity", 1);
            },
            update => update
                .transition().duration(750)
                .attr("transform", (d, i) => `translate(0,${barStep * i})`),
            exit => exit
                .transition().duration(750)
                .attr("opacity", 0)
                .remove()
            );
    
            bars.transition().duration(750)
                .attr("opacity", 1)
                .attr("transform", (d, i) => `translate(0,${barStep * i})`);

      x.domain([0, d3.max(d.children, d => d.value)]);
      svg.select(".x-axis")
        .transition()
        .duration(duration)
        .call(xAxis);
      
      firstRender = false;
    }
  
    function onDrillDown(node) {
      navigationPath.push(node);
      renderBreadcrumbs();
      render(node);
    }

    function renderBreadcrumbs() {
      const breadcrumbContainer = d3.select("#breadcrumb");
      breadcrumbContainer.selectAll("*").remove();

      navigationPath.forEach((node, index) => {
        breadcrumbContainer
          .append("span")
          .text(node.data.name)
          .style("cursor", "pointer")
          .on("click", () => {
            navigationPath = navigationPath.slice(0, index + 1);
            renderBreadcrumbs();
            render(node);
          });

        if (index < navigationPath.length - 1) {
          breadcrumbContainer.append("span").text(" > ");
        }
      });
    }

    function populateDropdowns(defaults) {
      const selects = d3.selectAll(".hierarchy-step").nodes();
      selects.forEach((select, i) => {
        const used = selects.slice(0, i).map(s => s.value);
        const available = allDimensions.filter(d => !used.includes(d));
        select.innerHTML = "";
        available.forEach(option => {
          const opt = document.createElement("option");
          opt.value = option;
          opt.text = option;
          select.appendChild(opt);
        });
        select.value = (defaults[i] && available.includes(defaults[i])) ? defaults[i] : "";
      });
    }
  
    function handleDropdownChange() {
      const selects = d3.selectAll(".hierarchy-step").nodes();
      const chosen = [];
      for (let i = 0; i < selects.length; i++) {
        const current = selects[i].value;
        const options = allDimensions.filter(d => !chosen.includes(d));
        selects[i].innerHTML = "";
        options.forEach(opt => {
          const o = document.createElement("option");
          o.value = opt;
          o.text = opt;
          selects[i].appendChild(o);
        });
        selects[i].value = current && options.includes(current) ? current : "";
        if (selects[i].value) chosen.push(selects[i].value);
      }
    }
  
    d3.selectAll(".hierarchy-step").on("change", handleDropdownChange);
    d3.select("#clear-hierarchy").on("click", () => {
      d3.selectAll(".hierarchy-step").property("value", "");
      populateDropdowns([]);
      
      navigationPath = [];
      root = null;

      d3.select("#breadcrumb").selectAll("*").remove(); // 🧹 Clear breadcrumb
      d3.select("#chart").selectAll("*").remove();       // 🧹 Clear chart
    });
  
    d3.select("#apply-hierarchy").on("click", () => {
      const selects = d3.selectAll(".hierarchy-step").nodes();
      const chosen = selects.map(s => s.value).filter(Boolean);
      //toggleAgeSortButton(chosen);

      if (chosen.length === 0) {
        navigationPath = [];
        root = null;
        d3.select("#breadcrumb").selectAll("*").remove();
        d3.select("#chart").selectAll("*").remove();
        return;
      }

      root = buildHierarchy(flatData, chosen);
      navigationPath = [root];
      
      // ❗ Drill down *only if* the first layer has only one child
      if (root.children && root.children.length === 1) {
        root = root.children[0];
        navigationPath.push(root);
      }

      renderBreadcrumbs();
      applySort(root, currentSortOption);
      render(root);
    });

    d3.select("#sort-select").on("change", function () {
      currentSortOption = this.value;
      applySort(root, currentSortOption);
      render(root);
    });
  
    d3.select("#back").on("click", () => {
      if (navigationPath.length > 1) {
        navigationPath.pop(); // Remove the current node
        const parentNode = navigationPath[navigationPath.length - 1]; // New current node
        root = parentNode;
        renderBreadcrumbs();
        applySort(root, currentSortOption);
        render(root);
      }
    });

    d3.select("#replay-animation").on("click", () => {
        // Step 1: Show Region-level view
        root = buildHierarchy(flatData, regionOnlyOrder);
        navigationPath = [root];
        renderBreadcrumbs();
        applySort(root, currentSortOption);
        firstRender = true;
        render(root);

        // Step 2: Auto transition to State view
        setTimeout(() => {
          svg.selectAll("g")
            .transition()
            .duration(500)
            .style("opacity", 0)
            .on("end", (_, i, nodes) => {
              if (i === nodes.length - 1) {
                root = buildHierarchy(flatData, defaultOrder);
                navigationPath = [root];

                if (root.children.length === 1) {
                  root = root.children[0];
                  navigationPath.push(root);
                }

                renderBreadcrumbs();
                applySort(root, currentSortOption);
                firstRender = true;
                render(root);
              }
            });
        }, 2500);
      });

    const data = await d3.csv("data/cleaned/norc_dementia_data_bar.csv");
    data.forEach(d => d.Count = +d.Count);
    flatData = data;
    root = buildHierarchy(flatData, regionOnlyOrder);
    navigationPath = [root];
    renderBreadcrumbs();
    applySort(root, currentSortOption);
    render(root);

    setTimeout(() => {
      // Fade out current Region view
      svg.selectAll("g")
        .transition()
        .duration(500)
        .style("opacity", 0)
        .on("end", (_, i, nodes) => {
          if (i === nodes.length - 1) { // only once after last bar fades out
            root = buildHierarchy(flatData, defaultOrder);
            navigationPath = [root];

            if (root.children.length === 1) {
              root = root.children[0];
              navigationPath.push(root);
            }

            renderBreadcrumbs();
            applySort(root, currentSortOption);
            render(root); // your existing function will handle fade-in
          }
        });
    }, 2500);

      // Populate the dropdowns using defaultOrder
      populateDropdowns(defaultOrder);
  });
  </script>
  
  <style scoped>
  .chart-wrapper {
    font-family: sans-serif;
  }

  ::v-deep(.label-text) {
  font-family: Arial, sans-serif;
  font-size: 12px;
  fill: #333;
}

::v-deep(.x-axis .tick text) {
  font-family: Arial, sans-serif;
  font-size: 12px;
  fill: #333;
}

  #tooltip {
    position: absolute;
    opacity: 0;
    pointer-events: none;
    background: #fff;
    border: 1px solid #ccc;
    padding: 6px 10px;
    font-size: 13px;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }

    .breadcrumb {
    font-family: Arial, sans-serif;
    font-size: 14px;
    margin-top: 20px;
    margin-bottom: 10px;
  }

  .breadcrumb span {
    color: #007bff;
  }

  .breadcrumb span:hover {
    text-decoration: underline;
  }

  </style>
  
