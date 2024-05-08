<script>
    export let data = []

</script>

<p>
    {#each data.oooorders as datapoint}
        {datapoint.product_code}
    {/each}
</p>
