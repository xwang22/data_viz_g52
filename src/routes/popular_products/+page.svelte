<script>
	// To create visualisations we need to know how large the image will be.
	const width = 436;
	const height = 300;
	// Also, we need to know how large the bars are
	const bar_width = 50;
	// And how far they are from each other
	const bar_distance = 100;
	// We usually reserve some space for the axes by specifying margins.
	const margin = { top: 10, right: 10, bottom: 50, left: 50 };
	// I call the remaining space the "content area". It tends to be useful
	// to give that space's size names as well.
	const inner_width = width - margin.left - margin.right;
	const inner_height = height - margin.top - margin.bottom;
		
	const rescale = function(x, domain_min, domain_max, range_min, range_max) {
  return ((range_max - range_min)*(x-domain_min))/(domain_max-domain_min) + range_min
  }
	
	// Number of top n elements to show
	const n = 10; 
	
	//export let data;
	
	//let products = processCSVData(data, n)
	export let data = [];
		
</script>

{JSON.stringify(data.products)}

<!-- Construct an SVG with the given width and height -->
<svg width={width} height={height} class="translated" transform="translate({margin.right}, {margin.top})">
		<rect x="0" 
					y="0" 
					width= {bar_width}
					height="50"/>
</svg>
	
	
	<style>
		svg {
			background-color: lightgrey;
		}
		rect {
			fill: teal;
		}
	</style>
