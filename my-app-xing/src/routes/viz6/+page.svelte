<script>
// Assuming data is an array of objects with fields "revenue", "order_year", "product_type", "account", and "region"
const data = [
    { revenue: 1000, order_year: 2019, product_type: "A", account: "X", region: "North" },
    { revenue: 1500, order_year: 2020, product_type: "B", account: "Y", region: "South" },
    { revenue: 1500, order_year: 2020, product_type: "B", account: "Y", region: "South" },
    // more data...
];

// Use reduce to group data by order_year and sum the revenue for all remaining combinations
const groupedData = data.reduce((result, entry) => {
    const { order_year, revenue, ...rest } = entry;
    const key = `${order_year}_${Object.values(rest).join('_')}`;
    if (!result[key]) {
        result[key] = {
            order_year,
            ...rest,
            revenue: 0
        };
    }
    result[key].revenue += revenue;
    return result;
}, {});

console.log(groupedData);
</script>