class Proxy {
  constructor (url, token) {
    this.url = url
    this.token = token
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

  getBetween (genus, from, to) {
    let fromStr = from.format('YYYY-MM-DD')
    let toStr = to.format('YYYY-MM-DD')
    let url = `${this.url}/between/${fromStr}/${toStr}?genus=${genus}`
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

  getSupportedLanguages () {
    return new Promise(resolve => {
      resolve(['en', 'de', 'lb', 'fr'])
    })
  }

  login (username, password) {
    let url = `${this.url}/auth`
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: username, password: password })
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
        return data.token
      })
  }

  setToken (token) {
    if (token === undefined) {
      debugger
    }
    this.token = token
  }

  upload (file) {
    let url = `${this.url}/upload`
    return fetch(url, {
      headers: {
        'Authorization': `JWT ${this.token}`
      }
    })
      .then(response => {
        if (response.status === 401) {
          throw new Error('Authorization failed')
        }
        return response.json()
      })
  }
}

export {
  Proxy
}
