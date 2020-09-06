<template>
  <q-page padding>
    <q-select
      v-model="genus"
      :options="options"
      :option-label="(item) => $t(item)"
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
      timelineData: [],
      timelineLayout: {
        barmode: 'stack',
        yaxis: { fixedrange: true },
        title: ''
      },
      heatmapData: [],
      heatmapLayout: {
        title: ''
      }
    }
  },
  methods: {
    filterGenera: function (value, update) {
      let self = this
      if (value === '') {
        update(() => {
          self.options = self.allValues
        })
        return
      }

      update(() => {
        const needle = value.toLowerCase()
        self.options = self.allValues.filter(v => {
          return (
            v.toLowerCase().indexOf(needle) > -1 ||
            self.$t(v).toLowerCase().indexOf(needle) > -1
          )
        })
      })
    },
    updateGenus: function (genus) {
      this.proxy.getRecent(genus)
        .then((data) => {
          this.timelineData = data
          this.timelineLayout.title = this.$t(genus)
          Plotly.react('Timeline', [this.timelineData], this.timelineLayout)
        })
      this.proxy.getHeatmap(genus)
        .then((data) => {
          this.heatmapData = data
          this.heatmapLayout.title = this.$t(genus)
          Plotly.react('Heatmap', [this.heatmapData], this.heatmapLayout)
        })
    }
  },
  watch: {
    genus: function (newValue, oldValue) {
      this.updateGenus(newValue)
    },
    locale: function (newValue) {
      this.heatmapLayout.title = this.$t(this.genus)
      this.timelineLayout.title = this.$t(this.genus)
      Plotly.setPlotConfig({ locale: newValue })
      Plotly.react(
        'Timeline', [this.timelineData], this.timelineLayout, { 'locale': newValue }
      )
      Plotly.react(
        'Heatmap', [this.heatmapData], this.heatmapLayout, { 'locale': newValue }
      )
    }
  },
  props: {
    locale: {
      type: String,
      required: true
    },
    proxy: {
      type: Object,
      required: true
    }
  },
  mounted () {
    Plotly.newPlot('Timeline', this.timelineData, this.timelineLayout)
    Plotly.newPlot('Heatmap', this.heatmapData, this.heatmapLayout)
    let self = this
    this.$refs.timelineRef.on('plotly_relayout', function (evt) {
      let from = moment(evt['xaxis.range[0]'])
      let to = moment(evt['xaxis.range[1]'])
      if (from - to === 0) {
        return
      }
      self.proxy.getBetween(self.genus, from, to)
        .then((data) => {
          this.timelineData = data
          Plotly.react('Timeline', [this.timelineData], this.timelineLayout)
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
