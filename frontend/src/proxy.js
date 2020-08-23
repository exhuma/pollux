class Proxy {
  constructor (url) {
    this.url = url
    console.log(url)
  }

  fetchGenera () {
    return fetch(`${this.url}/genera`)
      .then(response => {
        return response.json()
      })
  }

  getRecent (genus) {
    let url = `${this.url}/recent?num_days=365&genus=${genus}`
    return fetch(url)
      .then(response => {
        return response.json()
      })
      .then(data => {
        return data[genus]
      })
  }

  getHeatmap (genus) {
    let url = `${this.url}/heatmap/${genus}`
    return fetch(url)
      .then(response => {
        return response.json()
      })
      .then(data => {
        // JSON does not support NaN values. The backend return NaNs as -1.
        // Here we convert these back to proper NaN values so Plotly can
        // display them accordingly
        let tmp = []
        data.z.forEach((row) => {
          let mapped = row.map(cell => { return cell === -1 ? NaN : cell })
          tmp.push(mapped)
        })
        data.z = tmp
        return data
      })
  }
}

export {
  Proxy
}
