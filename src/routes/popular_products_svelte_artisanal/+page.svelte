<script>
    import { writable } from 'svelte/store';
	import * as d3 from 'd3';
	import {scaleOrdinal} from 'd3-scale';
	import {schemeCategory10} from 'd3-scale-chromatic';
    import { onMount } from 'svelte';

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

        // Create 'Other' product
        let otherProduct = {
            product_name: 'Other',
            type: 'Other',
            [`revenue`]: otherRevenue,
            [`quantity`]: otherQuantity
        };

        // Push 'Other' product to bestProducts
        bestProducts.push(otherProduct);

        // Filter out unwanted columns
        bestProducts = bestProducts.map(product => ({
                product_name: product.product_name,
                type: product.type,
                [`revenue`]: product[`revenue_${year}`],
                [`quantity`]: product[`quantity_${year}`]
            }));

        return bestProducts;
	}
	
	export let data;
		
	let n = 10; // Number of top n elements to show
	let typeselection = 'TOOLS & KITS'; // Which product types to show
	// Here the magic happens xD
    let year1 = 2019; // Example year
    let year2 = 2020; // Example year
    let year3 = 2021; // Example year
    let year4 = 2022; // Example year
    let year5 = 2023; // Example year
    
    // Change the definitions of bestProducts20XX to use writable stores
    let bestProducts2019 = [];
    let bestProducts2020 = [];
    let bestProducts2021 = [];
    let bestProducts2022 = [];
    let bestProducts2023 = [];

    // Update the arrays with new values when the component mounts
    bestProducts2019 = filterAndSelectProducts(typeselection, data, year1, n);
    bestProducts2020 = filterAndSelectProducts(typeselection, data, year2, n);
    bestProducts2021 = filterAndSelectProducts(typeselection, data, year3, n);
    bestProducts2022 = filterAndSelectProducts(typeselection, data, year4, n);
    bestProducts2023 = filterAndSelectProducts(typeselection, data, year5, n);

    console.log(bestProducts2019)
    console.log(bestProducts2020)
    console.log(bestProducts2021)
    console.log(bestProducts2022)
    console.log(bestProducts2023)
	let total = 40000000;

	// To create visualisations we need to know how large the image will be.
	const width = 436;
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


    // Function to calculate the y-coordinate based on cumulative height
	const calculateY = (bp, i) => {
        console.log(bp)
    if (i === 0) return height - rescale(bp.revenue, total, inner_height);
    console.log(i)
    // Calculate the cumulative height of previous bars in reverse order
    let cumulativeHeight = 0;
    const N = bp.length;
    for (let j = N - 1; j >= N - i; j--) {
        cumulativeHeight += bp[j].revenue;
    }
    console.log(cumulativeHeight)
    // Calculate the y-coordinate based on cumulative height
    return height - rescale(cumulativeHeight + bp.revenue, total, inner_height);
	};

    // Function to calculate the height of each bar
    const calculateHeight = (bp) => {
        return rescale(bp.revenue, total, inner_height);
    };

	// Function to assign color based on product_name
	const getColor = (product_name) => {
		// If the product_name is 'Other', return grey
		if (product_name === 'Other') {
			return 'grey'; // You can replace 'grey' with any other color code
		}
		// Otherwise, use the color scale
		const colorScale = d3.scaleOrdinal(d3.schemePaired);
		return colorScale(product_name);
	};

</script>

<!-- Construct an SVG with the given width and height -->
<svg width={width} height={height} class="translated" transform="translate({margin.right}, {margin.top + inner_height})">
    {#each bestProducts2019.slice().reverse() as bp, i}
        <!-- Calculate y position based on cumulativeHeight -->
        <rect
            x="50"
            y={calculateY(bp, i)}
            width={bar_width}
            height={calculateHeight(bp)}
            fill={getColor(bp.product_name)}
        ></rect>
    {/each}
    {#each bestProducts2020.slice().reverse() as bp, i}
        <!-- Calculate y position based on cumulativeHeight -->
        <rect
            x="150"
            y={calculateY(bp, i)}
            width={bar_width}
            height={calculateHeight(bp)}
            fill={getColor(bp.product_name)}
        ></rect>
    {/each}
    {#each bestProducts2021.slice().reverse() as bp, i}
    <!-- Calculate y position based on cumulativeHeight -->
    <rect
        x="250"
        y={calculateY(bp, i)}
        width={bar_width}
        height={calculateHeight(bp)}
        fill={getColor(bp.product_name)}
    ></rect>
    {/each}
    {#each bestProducts2022.slice().reverse() as bp, i}
    <!-- Calculate y position based on cumulativeHeight -->
    <rect
        x="350"
        y={calculateY(bp, i)}
        width={bar_width}
        height={calculateHeight(bp)}
        fill={getColor(bp.product_name)}
    ></rect>
    {/each}
    {#each bestProducts2023.slice().reverse() as bp, i}
    <!-- Calculate y position based on cumulativeHeight -->
    <rect
        x="450"
        y={calculateY(bp, i)}
        width={bar_width}
        height={calculateHeight(bp)}
        fill={getColor(bp.product_name)}
    ></rect>
    {/each}
</svg>