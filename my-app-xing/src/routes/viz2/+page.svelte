<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    // Sample data
    const data = [
      { type: 'A', region: 'X', revenue: 100 },
      { type: 'B', region: 'Y', revenue: 200 },
      { type: 'C', region: 'Z', revenue: 150 },
      // Add more data as needed
    ];
  
    let svg;
  
    // Prepare the chart on mount
    onMount(() => {
      // Set up SVG container
      svg = d3.select('svg');
  
      // Define scales
      const xScale = d3.scaleBand()
        .domain(data.map(d => d.type))
        .range([50, 350])
        .padding(0.1);
  
      const yScale = d3.scaleBand()
        .domain(data.map(d => d.region))
        .range([250, 50])
        .padding(0.1);
  
      // Create circles for each data point
      svg.selectAll('circle')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', d => xScale(d.type) + xScale.bandwidth() / 2)
        .attr('cy', d => yScale(d.region) + yScale.bandwidth() / 2)
        .attr('r', d => Math.sqrt(d.revenue) / Math.PI)
        .attr('fill', 'steelblue');
  
      // Add x-axis
      svg.append('g')
        .attr('transform', `translate(0, ${250})`)
        .call(d3.axisBottom(xScale));
  
      // Add y-axis
      svg.append('g')
        .attr('transform', `translate(${50}, 0)`)
        .call(d3.axisLeft(yScale));
    });
  </script>
  
  <svg width="400" height="300"></svg>