<script>
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
</script>
