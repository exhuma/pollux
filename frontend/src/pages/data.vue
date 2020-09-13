<template>
  <q-page padding>
    <DataTable
      :genera="selectedColumns"
      :data="data"
      ></DataTable>
    <h5>Select files to upload</h5>
    <q-uploader
      :url="proxy.upload_url"
      :filter="checkFileSize"
      :factory="makeHeaders"
      auto-upload
      @rejected="onRejected"
      @failed="onFailed"
      />
  </q-page>
</template>

<script>
import DataTable from 'src/components/DataTable.vue'
export default {
  props: {
    proxy: {
      type: Object,
      required: true
    }
  },
  created () {
    this.proxy.getRecentRaw()
      .then(responseData => {
        this.data = responseData
      })
  },
  data () {
    return {
      data: [],
      selectedColumns: []
    }
  },
  methods: {
    makeHeaders (files) {
      return {
        headers: [{ name: 'Authorization', value: `JWT ${this.proxy.token}` }]
      }
    },
    checkFileSize (files) {
      return files.filter(file => file.size < 16 * 16 * 1024)
    },
    onFailed (info) {
      this.$q.notify({
        type: 'negative',
        message: 'Unable to upload. Are you logged in?'
      })
    },
    onRejected (rejectedEntries) {
      this.$q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} file(s) were too large`
      })
    }
  },
  components: {
    DataTable
  }
}
</script>

<style>
</style>
