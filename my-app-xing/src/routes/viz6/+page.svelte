<script>
// Assuming data is an array of objects with fields "revenue", "order_year", "type", "account", and "region"
const data = [
    { revenue: 1000, revenue_19: 100,  type: "A", account: "X", region: "North" },
    { revenue: 1500, revenue_19: 100,  type: "B", account: "Y", region: "South" },
    { revenue: 1500, revenue_19: 100,  type: "B", account: "Y", region: "South" },
    // more data...
];

// Get all unique regions
let regions = [...new Set(data.map(item => item.region))];

let selectedRegion = "Select All"; // Default to "Select All"

let groupedData = []; // initialize groupedData

// Filter and group data based on the selected region
$: {
    let filteredData = selectedRegion === "Select All" ? data : data.filter(entry => entry.region === selectedRegion);

    let groupedData = filteredData.reduce((result, entry) => {
        const { type, account, revenue, revenue_19} = entry;
        const index = result.findIndex(item => item.type === type && item.account === account);

        if (index === -1) {
            result.push({
                type,
                account,
                revenue,
                revenue_19,
                growth: revenue / revenue_19
            });
        } else {
            result[index].revenue += revenue;
            result[index].revenue_19 += revenue_19;
            result[index].growth = result[index].revenue / result[index].revenue_19;
        }

        return result;
    }, []);

    console.log(groupedData); // Log groupedData after it's updated
}

</script>

<select bind:value={selectedRegion}>
    <option>Select All</option>
    {#each regions as region (region)}
        <option>{region}</option>
    {/each}
</select>