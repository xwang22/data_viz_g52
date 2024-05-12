export const load = async ({ fetch }) => {
    const responseViz1 = await fetch('https://raw.githubusercontent.com/xwang22/data_viz_g52/xing_data/data_viz1.json')
    const dataViz1 = await responseViz1.json()
    dataViz1.forEach((d,i) => { d.id = i })

    return {
      viz1: dataViz1
    }
}