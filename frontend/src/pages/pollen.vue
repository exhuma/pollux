<template>
  <q-page padding>
    <q-select
      v-model="genus"
      :options="options"
      label="Genus"
      use-input
      @filter="filterGenera"
      />
    <div id="Timeline" ref="timelineRef"></div>
    <div id="Heatmap"></div>
  </q-page>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly'
import moment from 'moment'
export default {
  data () {
    return {
      genus: 'Gramineae',
      allValues: [],
      options: [],
      timelineLayout: {
        barmode: 'stack',
        yaxis: { fixedrange: true },
        title: ''
      },
      heatmapLayout: {
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
          this.timelineLayout.title = genus
          Plotly.react('Timeline', [data], this.timelineLayout)
        })
      this.proxy.getHeatmap(genus)
        .then((data) => {
          this.heatmapLayout.title = genus
          Plotly.react('Heatmap', [data], this.heatmapLayout)
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
    Plotly.newPlot('Timeline', data, this.timelineLayout)
    Plotly.newPlot('Heatmap', data, this.heatmapLayout)
    let self = this
    this.$refs.timelineRef.on('plotly_relayout', function (evt) {
      let from = moment(evt['xaxis.range[0]'])
      let to = moment(evt['xaxis.range[1]'])
      if (from - to === 0) {
        return
      }
      self.proxy.getBetween(self.genus, from, to)
        .then((data) => {
          Plotly.react('Timeline', [data], this.timelineLayout)
        })
    })
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
