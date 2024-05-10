<script>
    export let data;
    import {extent} from "d3-array";
	import {scaleLinear} from "d3-scale";
    import {scalePoint} from "d3-scale";
    import {scaleSqrt} from "d3-scale";
    import {scaleSequential} from "d3-scale";
    import { interpolateRdYlGn } from 'd3-scale-chromatic';

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

     // find the unique count of product types and account types
     let productypes = [... new Set(parsed_data.map((d) => d.type))];
     let acounts = [... new Set(parsed_data.map((d) => d.account))];

     let rExtent = extent(parsed_data, (d)=> d.revenue);
     let gExtent =extent(parsed_data, (d)=> d.growth);
     console.log(rExtent);
    
    // we will start with a svg size of 500px by 500px
	 let width = 1000;
	 let height = 1000;
	 const margins = {top:20, right:20, bottom:20, left: 20};


     // make x and y linear scales
     let xScale = scalePoint().domain(productypes).range([margins.left, width - margins.right]);
	 let yScale = scalePoint().domain(acounts).range([height - margins.bottom, margins.top]); 
     let rScale = scaleSqrt().domain(rExtent).range([10,30]); 
     //let colorScale= scaleLinear().domain([-1,1]).range(["red","green"]); 
     //let colorScale = scaleSequential().domain([-1,1]).interpolator(interpolateRdYlGn); 
     let colorScale = scaleSequential().domain(gExtent).interpolator(interpolateRdYlGn); 

     console.log(rScale(Math.sqrt(216260/ Math.PI)))
</script>

<h1>Revenue per Product Type and Account Type</h1>

<svg {width} {height}>

	<g class="dots">
		{#each parsed_data as d}
			<circle cx={xScale(d.type)} cy={yScale(d.account)} r={rScale(d.revenue)} fill={colorScale(d.growth)}/>
		{/each}
	</g>
</svg>

<style>
	svg{
		background-color: white;
	}
	circle {
		/* fill: orange; */
		fill-opacity: 0.6;
		stroke: rgba(0,0,0,0.5);
	}

</style>