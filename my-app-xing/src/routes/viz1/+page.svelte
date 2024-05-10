<script>
    export let data;
    import {extent} from "d3-array";
	import {scaleLinear} from "d3-scale";
    //console.log(data)
    //change column names
	let parsed_data = data.viz1.map((d) => {
	 	return {
	 		type: d["Type"],
            account: d["Key Account"],
	 		revenue: d["ProductPricesInCP_split_23"],
			growth: d["growth_tot"]
	 	}
	 })
    // console.log(parsed_data)

    // find the max revenue
     let Extent = extent(parsed_data, (d)=> d.revenue);
     console.log(Extent);

     // find the unique count of product types and account types
     let productypes = [... new Set(parsed_data.map((d) => d.type))];
     let acounts = [... new Set(parsed_data.map((d) => d.account))];

     //let xExtent = productypes.length;
     //let yExtent = acounts.length;

     let xExtent = extent(parsed_data, (d)=> d.revenue);
     let yExtent =extent(parsed_data, (d)=> d.growth);

	//console.log("productypes", productypes.length);
    //console.log("acounts", acounts);
    
    // we will start with a svg size of 500px by 500px
	 let width = 1000;
	 let height = 1000;
	 const margins = {top:20, right:20, bottom:20, left: 20};


     // make x and y linear scales
	 let xScale = scaleLinear().domain(xExtent).range([margins.left, width - margins.right]);
	 let yScale = scaleLinear().domain(yExtent).range([height - margins.bottom, margins.top]); 

    // make ticks
	let xTicks = xScale.ticks(5);
	let yTicks = yScale.ticks(5);
	let xTickFormat = xScale.tickFormat(5, ".0s");
	let yTickFormat = yScale.tickFormat(5, ".2f");	

</script>

<h1>Revenue per Product Type and Account Type</h1>

<svg {width} {height}>
	<g class="x-axis">
		{#each xTicks as tick}
			<g class = "tick" transform='translate({xScale(tick)}, 0)'>
				<line y1={height - margins.bottom} y2={margins.top}/>
				<text y={height - margins.bottom + 16}>{xTickFormat(tick)}<text />
			</g>
		{/each}
	</g>
	
	<g class="y-axis">
		{#each yTicks as tick}
			<g class = "tick" transform='translate(0, {yScale(tick)})'>
				<line x1={margins.left} x2={width - margins.right}/>
				<text x={margins.left} y='+4'>{yTickFormat(tick)}<text />
			</g>
		{/each}
	</g>

	<g class="dots">
		{#each parsed_data as d}
			<circle cx={xScale(d.revenue)} cy={yScale(d.growth)} r='5'/>
		{/each}
	</g>
</svg>

<style>
	svg{
		background-color: black;
	}
	circle {
		fill: orange;
		fill-opacity: 0.6;
		stroke: rgba(0,0,0,0.5);
	}

    .tick line {
		stroke: #ddd;
		stroke-dasharray: 2;
	}
	text {
		font-size: 12px;
		fill: #999;
	}

	.x-axis text {
		text-anchor: middle;
	}

	.y-axis text {
		text-anchor: end;
	}

</style>