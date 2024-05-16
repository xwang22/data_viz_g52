<script>
	import * as d3 from 'd3';
	import {scaleOrdinal} from 'd3-scale';
	import {schemeCategory10} from 'd3-scale-chromatic';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { axisBottom, axisLeft } from 'd3-axis';

    let includeOther = true;

	function filterAndSelectProducts(typeselection, products, year, n, includeOther) {
        // Filter products based on typeselection

        let filteredProducts;
        if (typeselection == 'ALL') {
            filteredProducts = products.products;
        } else {
            filteredProducts = products.products.filter(products => products.type == typeselection);
        }

        // Sort filtered products by revenue for the given year
        let sortedProducts = filteredProducts.sort((a, b) => b[`revenue_${year}`] - a[`revenue_${year}`]);

        // Select the first n products
        let bestProducts = sortedProducts.slice(0, n);

        // Calculate total revenue for the given year
		let total = filteredProducts.reduce((acc, product) => acc + (product[`revenue_${year}`] || 0), 0);

        let otherRevenue = 0;
        let otherQuantity = 0;        

        if(includeOther){
            // Calculate total revenue and quantity for the remaining products
            for (let i = n; i < sortedProducts.length; i++) {
                otherRevenue += sortedProducts[i][`revenue_${year}`];
                otherQuantity += sortedProducts[i][`quantity_${year}`];
            }        
        }else{
            otherRevenue = 0;
            otherQuantity = 0;                    
        }

        // Create 'Other' product
        let otherProduct = {
                product_name: 'Other',
                type: 'Other',
                [`revenue`]: otherRevenue,
                [`quantity`]: otherQuantity
        }
        
        // Filter out unwanted columns
        bestProducts = bestProducts.map(product => ({
                product_name: product.product_name,
                type: product.type,
                [`revenue`]: product[`revenue_${year}`],
                [`quantity`]: product[`quantity_${year}`]
            }));

        
        // Push 'Other' product to bestProducts
        bestProducts.push(otherProduct);
        

        return bestProducts;
	}
	
	export let data;
		
	let n = 10; // Number of top n elements to show
	let typeselection = 'ALL'; // Which product types to show
	let total = 0;
	// To create visualisations we need to know how large the image will be.
	const width = 1200;
	const height = 900;
	// We usually reserve some space for the axes by specifying margins.
	const margin = { top: 40, right: 20, bottom: 100, left: 80 };
	// I call the remaining space the "content area". It tends to be useful
	// to give that space's size names as well.
	const inner_width = width - margin.left - margin.right;
	const inner_height = height - margin.top - margin.bottom;
	// Also, we need to know how large the bars are
	const bar_width = width / 8;
	// And how far they are from each other
	const bar_distance = (inner_width - bar_width * 5)/4;
		
	const rescale = function(x, maxvalue, maxheight) {
  		return (x / maxvalue * maxheight)
  	}

	// Function to calculate the x-coordinate based on the year and size of the bar
	const calculateX = (margin, year, bar_width, bar_distance) => {
		return margin.left + (year-2019) * (bar_width + bar_distance)
	}

    // Create a list of custom colors
    const customColors = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", 
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5", "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
    "#393b79", "#5254a3", "#6b6ecf", "#9c9ede", "#637939", "#8ca252", "#b5cf6b", "#cedb9c", "#8c6d31", "#bd9e39",
    "#e7ba52", "#e7cb94", "#843c39", "#ad494a", "#d6616b", "#e7969c", "#7b4173", "#a55194", "#ce6dbd", "#de9ed6"
    ];

    // Create a color scale
    const colorScale = d3.scaleOrdinal(customColors);

	// Function to assign color based on product_name
	const getColor = (product_name) => {
		// If the product_name is 'Other', return grey
		if (product_name === 'Other') {
			return 'lightgrey'; // You can replace 'grey' with any other color code
		}
		// Otherwise, use the color scale
		return colorScale(product_name);
	};

    function handleSliderInput(event) {
        n = parseInt(event.target.value); // Update the value of n
        updateVisualization(); // Update the visualization with the new value of n
    }

    // Function to handle dropdown selection
    function handleDropdownChange(event) {
        typeselection = event.target.value; // Update the value of typeselection
        updateVisualization(); // Update the visualization with the new value of typeselection
    }

    function handleToggleChange(event) {
    includeOther = event.target.checked;
    updateVisualization();
    }

    // Create a writable store to hold the HTML content
    const stackedBarsHTMLStore = writable('');

    function updateVisualization(){
        // Construct SVG for the current year
        let newstackedBarsHTML = `<svg width="${width}" height="${height}" class="translated" transform="translate(${margin.left}, ${margin.top})">`;
        //Re-initialize total
        let total = 0;
        
        const years4total = [2019, 2020, 2021, 2022, 2023];
        years4total.forEach(year4total => {
            
            // Filter and select products for the current year
            const bestProducts = filterAndSelectProducts(typeselection, data, year4total, n, includeOther);            
            // Calculate total revenue for the current year
            let yeartotal = bestProducts.reduce((acc, product) => acc + product.revenue, 0);
            console.log(yeartotal)
            // Compare with maxTotal and update if necessary
            if (yeartotal > total) {
                total = yeartotal;
            }
        })
        // Loop through each year and create stacked bars
        const years = [2019, 2020, 2021, 2022, 2023];
        years.forEach(year => {
            // Filter and select products for the current year
            const bestProducts = filterAndSelectProducts(typeselection, data, year, n, includeOther);

            // Loop through each product for the current year
            bestProducts.slice().reverse().forEach((bp, i) => {
                // Calculate x position based on size of the bars
                const x = calculateX(margin, year, bar_width, bar_distance);
                let y = 0;
                // Calculate y position based on cumulativeHeight
                if (i == 0){
                    y = margin.top + inner_height - rescale(bp.revenue, total, inner_height);
                }else{
                    let cumulativeHeight = 0;
                    const N = bestProducts.length;
                    for (let j = N - 1 ; j >= N - i; j--) {
                        const revenue = parseFloat(bestProducts[j].revenue);
                        cumulativeHeight += revenue;
                    }
                y = margin.top + inner_height - rescale(cumulativeHeight + bp.revenue, total, inner_height);
                }
                // Construct rect element for the current product
                const rectHTML = `<rect class="bar" x="${x}" y="${y}" width="${bar_width}" height="${rescale(bp.revenue, total, inner_height)}" fill="${getColor(bp.product_name)}"
                                data-product_name="${bp.product_name}"
                                onmouseover="document.getElementById('tooltip').style.opacity='1'; 
                                            document.getElementById('tooltip').innerHTML='${bp.product_name}, ${bp.revenue/1000000} MCP'; 
                                            document.getElementById('tooltip').style.left=event.pageX + 10 + 'px'; 
                                            document.getElementById('tooltip').style.top=event.pageY - 28 + 'px';"
                                            this.setAttribute('fill-opacity', 0.5);"                                            
                                onmouseout="document.getElementById('tooltip').style.opacity='0';
                                            this.setAttribute('fill-opacity', 1);"></rect>`;

                // Append rect element to SVG HTML
                newstackedBarsHTML += rectHTML;
            });

        });

        // Close group container for bars
        newstackedBarsHTML += `<g class="bars"></g>`        

        // Values to relocate the x axis so that the labels of the years fall exactly in the middle of the bars
        let xlimit_left = 2019 - ((bar_width/2) /  (bar_width + bar_distance));
        let xlimit_right = 2023 + ((bar_width/2) /  (bar_width + bar_distance));

        let xScale = d3.scaleLinear()
                        .domain([xlimit_left, xlimit_right]) // input 2019, 2020, 2021, 2022, 2023
                        .range([0, inner_width]); // output 

        let yScale = d3.scaleLinear()
                        .domain([0, total/1000000])  // input
                        .range([inner_height, 0]); // output 

        
        // Create a temporary SVG element for axes
        const tempSvg = d3.select(document.createElementNS(d3.namespaces.svg, 'svg'));

        // Append x-axis
        tempSvg.append('g')
            .attr('transform', `translate(${margin.left},${inner_height + margin.top})`)
            .call(d3.axisBottom(xScale).tickFormat(d3.format("")) // Format ticks as integers without any decimal points
                .ticks(5))
            .style('font-size', '20px');

        // Append y-axis
        tempSvg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`)
            .style('font-size', '20px')
            .call(d3.axisLeft(yScale)
                .ticks(5)) // adjust the number of ticks if needed
            
        
        tempSvg.append('text')
            .attr('x', -(inner_height / 2))
            .attr('y', margin.left / 3)
            .attr('transform', 'rotate(-90)')
            .attr('text-anchor', 'middle')
            .text('Revenues [MCP]')
            .style('font-size', '24px'); // Adjust font size if needed

        // Add axes HTML to stackedBarsHTML
        newstackedBarsHTML += tempSvg.html();

        // Close SVG tag
        newstackedBarsHTML += `</svg>`;

        // Update the value of the store with the new HTML content
        stackedBarsHTMLStore.set(newstackedBarsHTML);
    }

    onMount(updateVisualization);

</script>

<h1> Revenues coming from the top n products (per product type) over time </h1>

<div style="font-size: 24px">
    <label for="slider">Number of n Top Elements:</label>
    <input type="range" id="slider" min="3" max="20" step="1" bind:value={n} on:input={handleSliderInput}>
    <span>{n}</span>
</div>

<div style="font-size: 24px">
    <label for="typeselection">Product Type Selection:</label>
    <select id="typeselection" bind:value={typeselection} on:change={handleDropdownChange}>
        <option value="ALL">All Products</option>
        <option value="ADVENTURING EQUIPMENT">Adventuring Equipment</option>
        <option value="ANIMALS & TRANSPORTATION">Animals & Transportation</option>
        <option value="ARMS & ARMOUR">Arms & Armour</option>        
        <option value="JEWELRY">Jewelry</option>
        <option value="MUSICAL INSTRUMENT">Musical Instrument</option>
        <option value="POTIONS & SCROLLS">Potions & Scrolls</option>
        <option value="SUMMONING DEVICE">Summoning Device</option>
        <option value="TOOLS & KITS">Tools & Kits</option>
        <!-- Add more options as needed -->
    </select>
</div>

<div style="font-size: 24px">
    <label for="toggle">Include 'Other' Component:</label>
    <input type="checkbox" id="toggle" bind:checked={includeOther} on:change={handleToggleChange}>
</div>

{@html $stackedBarsHTMLStore}

<style>
    .tooltip {
      position: absolute;
      text-align: center;
      padding: 5px;
      font-size: 16px;
      background: rgb(240, 239, 240);
      border: 0px solid;
      border-radius: 5px;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.2s;
    }
</style>

<div id="tooltip" class="tooltip"></div>