<template>
  <q-page padding>
    <q-select
      v-model="genus"
      :options="options"
      label="Genus"
      use-input
      @filter="filterGenera"
      />
    <div id="Graph"></div>
  </q-page>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly'
export default {
  data () {
    return {
      genus: 'Gramineae',
      allValues: [],
      options: [],
      graphLayout: {
        barmode: 'stack',
        yaxis: { fixedrange: true },
        title: ''
      }
    }
  },
  methods: {
    filterGenera: function (value, update) {
      if (value === '') {
        update(() => {
          this.options = this.allValues
        })
        return
      }

      update(() => {
        const needle = value.toLowerCase()
        this.options = this.allValues.filter(v => v.toLowerCase().indexOf(needle) > -1)
      })
    },
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
        this.allValues = data
      })
  }
}
</script>

<style>
</style>
