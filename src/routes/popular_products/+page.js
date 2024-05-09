import Papa from 'papaparse'

export const load = async ({ fetch }) => {
 
  const responseProducts = await fetch('https://github.com/xwang22/data_viz_g52/blob/andrea_testing/static/final_v2_df.csv', {
    headers: {
      'Content-Type': 'text/csv'
  }})
  let csvProducts = await responseProducts.text()
  let parsedCsvProducts = Papa.parse(csvProducts, {header: true})

  return {
    products: parsedCsvProducts.data
  }
}