import Papa from 'papaparse'

export const load = async ({ fetch }) => {
  const orders = await fetch('https://raw.githubusercontent.com/JannesPeeters/DEAD/main/data/orders.csv', {
      headers: {
        'Content-Type': 'text/csv'
    }})
    let oorders = await orders.text()
    let ooorders = Papa.parse(oorders, {header: true})

    return {
      oooorders: ooorders.data
    }
}