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
      options: ['Acer', 'Gramineae'],
      graphLayout: {
        barmode: 'stack',
        yaxis: { fixedrange: true }
      }
    }
  },
  watch: {
    model: function (newValue, oldValue) {
      let url = `http://localhost:5000/recent?num_days=200&genus=${newValue}`
      let that = this
      this.$axios.get(url).then(response => {
        let values = response.data[newValue]
        let data = [values]
        Plotly.react('Graph', data, that.graphLayout)
      })
    }
  },
  mounted () {
    var data = []
    Plotly.newPlot('Graph', data, this.graphLayout)
  },
  created () {
    let url = 'http://localhost:5000/recent?num_days=200&genus=Acer'
    let that = this
    this.$axios.get(url).then(response => {
      let acer = response.data['Acer']
      let data = [acer]
      Plotly.react('Graph', data, that.graphLayout)
    })
  }
}
</script>

<style>
</style>
