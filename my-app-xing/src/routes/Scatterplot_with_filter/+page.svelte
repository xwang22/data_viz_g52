<script>
    export let data;
    import {extent} from "d3-array";
	import {scaleLinear} from "d3-scale";
    import {scalePoint} from "d3-scale";
    import {scaleSqrt} from "d3-scale";
    import {scaleSequential} from "d3-scale";
    import { interpolatePiYG } from 'd3-scale-chromatic';
	import { axisBottom } from 'd3-axis';

    //==================================Start importing region level data==================================
    let parsed_data_reg = data.viz1_region.map((d) => {
	 	return {
            id: d["id"],
	 		type: d["Type"],
            account: d["Key Account"],
	 		revenue: d["ProductPricesInCP_split_23"],
			revenue_19: d["ProductPricesInCP_split_19"],
			growth: d["growth_tot"],
			region: d["Region"]
	 	}
	 })

// allow region selection
let regions = [...new Set(parsed_data_reg.map(item => item.region))];
let selectedRegion = "select a region"; // Default selection

//groupby type and account after region selection
let groupedData = []; // initialize groupedData

// Filter and group data based on the selected region
$: {
	// Drop the growth column
    let dataWithoutGrowth = parsed_data_reg.map(({ growth, ...rest }) => rest); 
    // filter for region based on selection
    let filteredData = selectedRegion === "select a region" ? dataWithoutGrowth : dataWithoutGrowth.filter(entry => entry.region === selectedRegion);
    // group by type and account
    groupedData = filteredData.reduce((result, entry) => {
        const { type, account, revenue, revenue_19} = entry;
        const index = result.findIndex(item => item.type === type && item.account === account);

        if (index === -1) {
            result.push({
                type,
                account,
                revenue,
                revenue_19,
                growth: revenue / revenue_19 - 1
            });
        } else {
            result[index].revenue += revenue;
            result[index].revenue_19 += revenue_19;
            result[index].growth = result[index].revenue / result[index].revenue_19 - 1;
        }

        return result;
    }, []);
    // add the id column, drop the revenue_19 column
	groupedData = groupedData.map(({ revenue_19, ...rest }, index) => ({ id: index + 1, ...rest }));

    // sort data according to revenue
    groupedData.sort((a, b) => a.revenue - b.revenue);

    //console.log(groupedData); // Log groupedData after it's updated
}

console.log(groupedData);
    //==================================End importing region level data==================================

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
    //console.log(parsed_data)

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
     //let colorScale = scaleSequential().domain([-1,1]).interpolator(interpolatePiYG); 
     let colorScale = scaleSequential().domain(gExtent).interpolator(interpolatePiYG); 

     const xticks = productypes;
	 const yticks = acounts;
	 //console.log(gExtent);
	 //console.log(colorScale(0.4));

     // record mouse position for hover
     let selected_datapoint = undefined;
     let mouse_x,mouse_y;
     const setMousePosition = function(event){
        mouse_x = event.clientX;
        mouse_y = event.clientY;
     }

</script>

<h1>Revenue per Product Type and Account Type</h1>

<select bind:value={selectedRegion}>
    <option>select a region</option>
    {#each regions as region (region)}
        <option>{region}</option>
    {/each}
</select>

<svg {width} {height}>

	<g transform="translate({margins.left},{margins.top})">
		{#each groupedData as d}
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
    select{position: relative;
    top: -800px; /* Adjust this value as needed */}

</style>