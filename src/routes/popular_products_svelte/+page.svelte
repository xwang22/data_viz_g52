<script>
	import * as d3 from 'd3';
	import {scaleOrdinal} from 'd3-scale';
	import {schemeCategory10} from 'd3-scale-chromatic';
    import { onMount } from 'svelte';
    import { writable } from 'svelte/store';
    import { axisBottom, axisLeft } from 'd3-axis';

	function filterAndSelectProducts(typeselection, products, year, n) {
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

        // Calculate total revenue and quantity for the remaining products
        let otherRevenue = 0;
        let otherQuantity = 0;
        for (let i = n; i < sortedProducts.length; i++) {
            otherRevenue += sortedProducts[i][`revenue_${year}`];
            otherQuantity += sortedProducts[i][`quantity_${year}`];
        }

        // Filter out unwanted columns
        bestProducts = bestProducts.map(product => ({
                product_name: product.product_name,
                type: product.type,
                [`revenue`]: product[`revenue_${year}`],
                [`quantity`]: product[`quantity_${year}`]
            }));

        // Create 'Other' product
        let otherProduct = {
            product_name: 'Other',
            type: 'Other',
            [`revenue`]: otherRevenue,
            [`quantity`]: otherQuantity
        };

        // Push 'Other' product to bestProducts
        bestProducts.push(otherProduct);

        return bestProducts;
	}
	
	export let data;
		
	let n = 10; // Number of top n elements to show
	let typeselection = 'TOOLS & KITS'; // Which product types to show
	let total = 0;
	// To create visualisations we need to know how large the image will be.
	const width = 100;
	const height = 300;
	// We usually reserve some space for the axes by specifying margins.
	const margin = { top: 10, right: 10, bottom: 50, left: 50 };
	// I call the remaining space the "content area". It tends to be useful
	// to give that space's size names as well.
	const inner_width = width - margin.left - margin.right;
	const inner_height = height - margin.top - margin.bottom;
	// Also, we need to know how large the bars are
	const bar_width = 50;
	// And how far they are from each other
	const bar_distance = (inner_width - bar_width * 5)/4;
		
	const rescale = function(x, maxvalue, maxheight) {
  		return (x / maxvalue * maxheight)
  	}

	// Function to calculate the x-coordinate based on the year and size of the bar
	const calculateX = (margin, year, bar_width, bar_distance) => {
		return margin.right + (year-2019) * (bar_width + bar_distance)
	}

    // Function to calculate the height of each bar
    const calculateHeight = (bp) => {
        return rescale(bp.revenue, total, inner_height);
    };

    // Create a color scale
    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

	// Function to assign color based on product_name
	const getColor = (product_name) => {
		// If the product_name is 'Other', return grey
		if (product_name === 'Other') {
			return 'grey'; // You can replace 'grey' with any other color code
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

    // Create a writable store to hold the HTML content
    const stackedBarsHTMLStore = writable('');

    function updateVisualization(){
        let newstackedBarsHTML = ''; // Initialize a new variable to hold the HTML content
        // Construct SVG for the current year
        let svgHTML = `<svg width="${width}" height="${height}" class="translated" transform="translate(${margin.left}, ${margin.top})">`;
        // Re-initialize the value of total
        total = 0;
        // Loop through each year and create stacked bars
        const years = [2019, 2020, 2021, 2022, 2023];
        years.forEach(year => {
            // Filter and select products for the current year
            const bestProducts = filterAndSelectProducts(typeselection, data, year, n);
            console.log(bestProducts)

            // Calculate total revenue for the current year
            let yeartotal = bestProducts.reduce((acc, product) => acc + product.revenue, 0);

            // Compare with maxTotal and update if necessary
            if (yeartotal > total) {
                total = yeartotal;
            }
            // Construct SVG for the current year
            let svgHTML = `<svg width="${width}" height="${height}" class="translated" transform="translate(${margin.left}, ${margin.top})">`;

            // Loop through each product for the current year
            bestProducts.slice().reverse().forEach((bp, i) => {
                // Calculate x position based on size of the bars
                const x = calculateX(margin, year, bar_width, bar_distance);
                let y = 0;
                // Calculate y position based on cumulativeHeight
                if (i == 0){
                    y = height - rescale(bp.revenue, total, inner_height);
                    //console.log(y)
                }else{
                    let cumulativeHeight = 0;
                    const N = bestProducts.length;
                    for (let j = N - 1 ; j >= N - i; j--) {
                        const revenue = parseFloat(bestProducts[j].revenue);
                        cumulativeHeight += revenue;
                    }
                y = height - rescale(cumulativeHeight + bp.revenue, total, inner_height);
                //console.log(y)
                }

                // Construct rect element for the current product
                const rectHTML = `<rect x="${x}" y="${y}" width="${bar_width}" height="${calculateHeight(bp)}" fill="${getColor(bp.product_name)}"></rect>`;

                // Append rect element to SVG HTML
                svgHTML += rectHTML;
            });

        // Close SVG tag
        svgHTML += `</svg>`;

        // Add SVG HTML for the current year to stackedBarsHTML
        newstackedBarsHTML += svgHTML;

        });


        // Update the value of the store with the new HTML content
        stackedBarsHTMLStore.set(newstackedBarsHTML);
    }

    onMount(updateVisualization);

</script>

<div>
    <label for="slider">Number of Top Elements (n):</label>
    <input type="range" id="slider" min="3" max="20" step="1" bind:value={n} on:input={handleSliderInput}>
    <span>{n}</span>
</div>

<div>
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

{@html $stackedBarsHTMLStore}