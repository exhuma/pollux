<template>
  <q-page padding>
    <q-select v-model="genus" :options="options" label="Genus" />
    <div id="Graph"></div>
  </q-page>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly'
export default {
  data () {
    return {
      genus: null,
      options: ['Acer', 'Gramineae'],
      graphLayout: {
        barmode: 'stack',
        yaxis: { fixedrange: true }
      }
    }
  },
  watch: {
    genus: function (newValue, oldValue) {
      this.proxy.getRecent(newValue)
        .then((data) => {
          Plotly.react('Graph', [data], this.graphLayout)
        })
    }
  },
  props: {
    proxy: {
      type: Object,
      required: true
    }
  },
  mounted () {
    var data = []
    Plotly.newPlot('Graph', data, this.graphLayout)
  },
  created () {
    this.proxy.getRecent('Acer')
      .then((data) => {
        Plotly.react('Graph', [data], this.graphLayout)
      })
    this.proxy.fetchGenera()
      .then(data => {
        this.options = data
      })
  }
}
</script>

<style>
</style>
