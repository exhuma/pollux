<template>
  <q-table
    :data="rows"
    :columns="columns"
    :hide-bottom="hide_bottom"
    row-key="date"
    >
    <template v-slot:body-cell="props">
      <q-td :props="props" :class="(props.value === 0 ? 'greyed' : '')">{{ props.value }}</q-td>
    </template>
  </q-table>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    hide_bottom: {
      type: Boolean,
      required: false,
      default: false
    },
    genera: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      required: true
    }
  },
  computed: {
    columns: function () {
      if (this.data && this.data.length === 0) {
        return []
      }
      let firstRow = this.data[0]
      let columns = [{
        name: 'date',
        label: 'Date',
        field: 'date',
        sortable: true,
        style: 'width: 100px'
      }]
      console.log(this.genera)
      for (const entry of Object.entries(firstRow)) {
        if (
          entry[0].toLowerCase() === 'date' ||
          (this.genera.length > 0 && !this.genera.includes(entry[0]))
        ) {
          continue
        }
        columns.push({
          name: entry[0].toLowerCase(),
          label: entry[0],
          field: entry[0],
          align: 'right'
        })
      }
      return columns
    },
    rows: function () {
      if (this.data && this.data.length === 0) {
        return []
      }
      return this.data
    }

  }
}
</script>

<style>
.greyed {
  color: #cecece;
}
</style>
