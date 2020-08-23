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
      genus: 'Gramineae',
      options: ['Acer', 'Gramineae'],
      graphLayout: {
        barmode: 'stack',
        yaxis: { fixedrange: true },
        title: ''
      }
    }
  },
  methods: {
    updateGenus: function (genus) {
      this.proxy.getRecent(genus)
        .then((data) => {
          this.graphLayout.title = genus
          Plotly.react('Graph', [data], this.graphLayout)
        })
    }
  },
  watch: {
    genus: function (newValue, oldValue) {
      this.updateGenus(newValue)
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
    this.updateGenus(this.genus)
    this.proxy.fetchGenera()
      .then(data => {
        this.options = data
      })
  }
}
</script>

<style>
</style>
