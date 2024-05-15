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
            id: d["id"],
	 		type: d["Type"],
            account: d["Key Account"],
	 		revenue: d["ProductPricesInCP_split_23"],
			growth: d["growth_tot"]
	 	}
	 })
     // sort data according to revenue
     parsed_data.sort((a, b) => a.revenue - b.revenue);
    // console.log(parsed_data)

     // find the unique count of product types and account types
     let productypes = [... new Set(parsed_data.map((d) => d.type))];
     let acounts = [... new Set(parsed_data.map((d) => d.account))];

     let rExtent = extent(parsed_data, (d)=> d.revenue);
     let gExtent =extent(parsed_data, (d)=> d.growth);
     //console.log(rExtent);
    
    // start with a svg
	 let width = 1200;
	 let height = 850;
	 const margins = {top:50, right:50, bottom:100, left: 200};
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

     // record mouse position for hover
     let selected_datapoint = undefined;
     let mouse_x,mouse_y;
     const setMousePosition = function(event){
        mouse_x = event.clientX;
        mouse_y = event.clientY;
     }

</script>

<h1>Revenue per Product Type and Account Type</h1>

<svg {width} {height}>

	<g transform="translate({margins.left},{margins.top})">
		{#each parsed_data as d}
			<circle cx={xScale(d.type)} cy={yScale(d.account)} r={rScale(d.revenue)} fill={colorScale(d.growth)}
				class:selected="{selected_datapoint && d.id == selected_datapoint.id}"
                on:mouseover = {function(event){selected_datapoint = d; setMousePosition(event)}}
                on:mouseout = {function(){selected_datapoint = undefined}}
			/>
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
				<text x={xScale(tick)} y = 20 style = "font-size: 10px; text-anchor: middle;">
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
				<text y={yScale(tick)} x = -3, style = "font-size: 12px; alignment-baseline:middle; text-anchor: end; ">
				{tick}
				</text>
			{/each}
		</g>
		
	</g>
</svg>

{#if selected_datapoint!=undefined}
<div id='tooltip' style = "left: {mouse_x + 10}px; top:{mouse_y-10}px">
Account: {selected_datapoint.account}<br/>
Product Type: {selected_datapoint.type}<br/>
Revenue 2023: {selected_datapoint.revenue}<br/>
Growth from 2019: {selected_datapoint.growth}
</div>
{/if}

<style>
	svg{
		background-color: white;
	}
	circle {
		/* fill: orange; */
		fill-opacity: 0.6;
		stroke: rgba(0,0,0,0.5);
	}
    /* define hover format */
    circle.selected{
        fill:black;
        fill-opaciy:1;
    }
    #tooltip{
        position:fixed;
        background-color: white;
        padding: 3px;
        border: solid 1px;
    }

</style>