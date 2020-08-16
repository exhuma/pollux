<template>
  <q-page padding>
    <q-select v-model="model" :options="options" label="Standard" />
    <div id="Graph"></div>
  </q-page>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly'
export default {
  data () {
    return {
      model: null,
      options: ['Acer', 'Gramineae']
    }
  },
  watch: {
    model: function (newValue, oldValue) {
      let url = `http://localhost:5000/recent?num_days=200&genus=${newValue}`
      this.$axios.get(url).then(response => {
        let values = response.data[newValue]
        let data = [values]
        let layout = { barmode: 'stack' }
        Plotly.react('Graph', data, layout)
      })
    }
  },
  mounted () {
    var data = []
    var layout = { barmode: 'stack' }
    Plotly.newPlot('Graph', data, layout)
  },
  created () {
    let url = 'http://localhost:5000/recent?num_days=200&genus=Acer'
    this.$axios.get(url).then(response => {
      let acer = response.data['Acer']
      let data = [acer]
      let layout = { barmode: 'stack' }
      Plotly.react('Graph', data, layout)
    })
  }
}
</script>

<style>
</style>
