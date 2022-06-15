import {Moment} from 'moment';

class Proxy {
  token: string;
  url: string;
  upload_url: string;

  constructor (url: string, token: string) {
    this.url = url
    this.token = token
    this.upload_url = url + '/upload'
  }

  async fetchGenera (): Promise<any> {
    let response = await fetch(`${this.url}/genera`)
    return response.json()
  }

  async getRecent (genus: string): Promise<any> {
    let url = `${this.url}/recent?num_days=365&genus=${genus}`
    let response = await fetch(url, {
      headers: {
        'Accept': 'application/prs.plotlydict+json'
      }
    })
    let data: any = response.json();
    return data[genus]
  }

  async getRecentRaw (): Promise<any> {
    let url = `${this.url}/recent?num_days=5`
    let response = await fetch(url, {
      headers: {
        'Accept': 'application/json'
      }
    })
    return response.json()
  }

  async getBetween (genus: string, from: Moment, to: Moment): Promise<any> {
    let fromStr = from.format('YYYY-MM-DD')
    let toStr = to.format('YYYY-MM-DD')
    let url = `${this.url}/between/${fromStr}/${toStr}?genus=${genus}`
    let response = await fetch(url, {
      headers: {
        'Accept': 'application/prs.plotlydict+json'
      }
    })
    let data = await response.json()
    return data[genus]
  }

  async getHeatmap (genus: string) {
    let url = `${this.url}/heatmap/${genus}`
    let response = await fetch(url)
    let data = await response.json()

    // JSON does not support NaN values. The backend return NaNs as -1.
    // Here we convert these back to proper NaN values so Plotly can
    // display them accordingly
    let tmp: number[][] = []
    data.z.forEach((row: number[]) => {
      let mapped = row.map(cell => { return cell === -1 ? NaN : cell })
      tmp.push(mapped)
    })
    data.z = tmp
    return data
  }

  getSupportedLanguages (): Promise<string[]> {
    return new Promise(resolve => {
      resolve(['en', 'de', 'lb', 'fr'])
    })
  }

  async login (username: string, password: string): Promise<string> {
    let url = `${this.url}/auth`
    let response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username: username, password: password })
    })
    let data = await response.json()
    return data.token
  }

  setToken (token: string): void {
    this.token = token
  }

  async upload (file: string): Promise<any> {
    let url = `${this.url}/upload`
    let response = await fetch(url, {
      headers: {
        'Authorization': `JWT ${this.token}`
      }
    })
    if (response.status === 401) {
      throw new Error('Authorization failed')
    }
    return response.json()
  }
}

export {
  Proxy
}
