export const load = async ({ fetch }) => {
 
  const productsRes = await fetch('https://raw.githubusercontent.com/xwang22/data_viz_g52/andrea_testing/static/final_v2_df.json')
  const productData = await productsRes.json()
  //const products = productData.products
 
  return {
    products: productData
  }
}