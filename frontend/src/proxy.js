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
}

export {
  Proxy
}
