<script>
    export let data;
    import {extent} from "d3-array";
	import {scaleLinear} from "d3-scale";
    import {scalePoint} from "d3-scale";
    import {scaleSqrt} from "d3-scale";
    import {scaleSequential} from "d3-scale";
    import { interpolateRdYlGn } from 'd3-scale-chromatic';
	import { axisBottom } from 'd3-axis';

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
     //console.log(rExtent);
    
    // start with a svg
	 let width = 1200;
	 let height = 800;
	 const margins = {top:20, right:50, bottom:100, left: 200};
	 const innerWidth = width - margins.left - margins.right;
 	 const innerHeight = height - margins.top - margins.bottom;

     // make x and y linear scales
     let xScale = scalePoint().domain(productypes).range([0, innerWidth]);
	 let yScale = scalePoint().domain(acounts).range([innerHeight, 0]); 
     let rScale = scaleSqrt().domain(rExtent).range([10,30]); 
     //let colorScale= scaleLinear().domain([-1,1]).range(["red","green"]); 
     //let colorScale = scaleSequential().domain([-1,1]).interpolator(interpolateRdYlGn); 
     let colorScale = scaleSequential().domain(gExtent).interpolator(interpolateRdYlGn); 

     const xticks = productypes;
	 const yticks = acounts;
	 console.log(gExtent);
	 console.log(colorScale(0.4));

</script>

<h1>Revenue per Product Type and Account Type</h1>

<svg {width} {height}>

	<g transform="translate({margins.left},{margins.top})">
		{#each parsed_data as d}
			<circle cx={xScale(d.type)} cy={yScale(d.account)} r={rScale(d.revenue)} fill={colorScale(d.growth)}>
				<title>My tooltip</title>
			</circle>
		{/each}

		 <!-- X Axis, 30 is the max radius-->
		 <g transform="translate(0, {innerHeight+30})"> 
			<line x1="0" y1="0" x2={innerWidth} y2="0" stroke="black"/>
			<text fill="black" x={innerWidth/2} y=50 style = "font-size: 16px; text-anchor: middle;">Product Type</text>
			{#each xticks as tick}
				<line
					x1={xScale(tick)}
					x2={xScale(tick)}
					y1=0
					y2=6
					stroke="black"
					/>
				<text x={xScale(tick)} y = 20 style = "font-size: 9px; text-anchor: middle;">
				{tick}
				</text>
			{/each}
		</g>

		<!-- Y Axis, 30 is the max radius-->
		<g transform="translate(-30, 0)"> 
			<line x1="0" y1="0" x2="0" y2={innerHeight+30} stroke="black"/>
			<text fill="black" x=-{innerHeight/2} y = -100 transform="rotate(-90)" style = "font-size: 16px; text-anchor:middle">Account</text>
			{#each yticks as tick}
				<line
					x1=0
					x2=6
					y1={yScale(tick)}
					y2={yScale(tick)}
					stroke="black"
					/>
				<text y={yScale(tick)} x = -3, style = "font-size: 10px; alignment-baseline:middle; text-anchor: end; ">
				{tick}
				</text>
			{/each}
		</g>
		
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