<script>
	// import YTPSelection from '../../components/YTPSelection.svelte';
	import { LayerCake, Svg, flatten, stack } from 'layercake';

  	import { scaleBand, scaleOrdinal } from 'd3-scale';
  	import { format } from 'd3-format';

 	import BarStacked from '../../components/BarStacked.svelte';
  	import AxisX from '../../components/AxisY.svelte';
  	import AxisY from '../../components/AxisX.svelte';

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
            [`revenue_${year}`]: otherRevenue,
            [`quantity_${year}`]: otherQuantity
        };

        // Push 'Other' product to bestProducts
        bestProducts.push(otherProduct);

        // Filter out unwanted columns
        bestProducts = bestProducts.map(product => ({
                product_name: product.product_name,
                type: product.type,
                [`revenue_${year}`]: product[`revenue_${year}`],
                [`quantity_${year}`]: product[`quantity_${year}`]
            }));

        return bestProducts;
	}
	
	export let data;
		
	let n = 10; // Number of top n elements to show
	let typeselection = 'TOOLS & KITS'; // Which product types to show
	let year = 2022; // Example year
  	let bestProducts2022 = filterAndSelectProducts(typeselection, data, year, n);
	console.log(bestProducts2022)

	const xKey = [0, 1];
  	const yKey = year;
  	const zKey = bestProducts2022.map(product => product.type);

	console.log(bestProducts2022)

	const seriesNames = bestProducts2022.map(product => product.product_name);
	const seriesColors = ['#00bbff', '#8bcef6', '#c4e2ed', '#f7f6e3', '#00bbff', '#8bcef6', '#c4e2ed', '#f7f6e3', '#00bbff', '#8bcef6', '#00bbff'];

	bestProducts2022.forEach(d => {
    	seriesNames.forEach(name => {
      		d[name] = +d[name];
    	});
  	});

  	const formatLabelX = d => format(`~s`)(d);

	const stackedData = stack(bestProducts2022, seriesNames);	
	
</script>

<style>
	/*
	  The wrapper div needs to have an explicit width and height in CSS.
	  It can also be a flexbox child or CSS grid element.
	  The point being it needs dimensions since the <LayerCake> element will
	  expand to fill it.
	*/
	.chart-container {
	  width: 100%;
	  height: 250px;
	}
</style>

<div class="chart-container">
	<LayerCake
	  padding={{ top: 0, bottom: 20, left: 35 }}
	  x={xKey}
	  y={yKey}
	  z={zKey}
	  yScale={scaleBand().paddingInner(0.05)}
	  zScale={scaleOrdinal()}
	  zDomain={seriesNames}
	  zRange={seriesColors}
	  flatData={flatten(stackedData)}
	  data={stackedData}
	>
	  <Svg>
		<AxisX
		  baseline
		  snapLabels
		  format={formatLabelX}
		/>
		<AxisY
		  gridlines={false}
		/>
		<BarStacked/>
	  </Svg>
	</LayerCake>
  </div>