<template>
  <q-layout view="hHh lpR fFf">

    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="leftDrawer = !leftDrawer" />

        <q-toolbar-title>
          Title
        </q-toolbar-title>
      </q-toolbar>

      <q-tabs align="left">
        <q-route-tab
          icon="map"
          to="/your/route"
          replace
          label="One Tab"
        />
        <q-route-tab
          icon="assignment"
          to="/some/other/route"
          replace
          label="Other Tab"
        />
      </q-tabs>
    </q-header>

    <q-drawer
      v-model="leftDrawer"
      side="left"
      bordered
      content-class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>Essential Links</q-item-label>

        <q-item to="/pollen" exact>
          <q-item-section avatar>
            <q-icon name="gps_fixed" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Pollen</q-item-label>
            <q-item-label caption>Pollen concentration</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/spores" exact>
          <q-item-section avatar>
            <q-icon name="bug_report" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Spores</q-item-label>
            <q-item-label caption>Spore Concentration</q-item-label>
          </q-item-section>
        </q-item>

        <q-item to="/information" exact>
          <q-item-section avatar>
            <q-icon name="school" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Information</q-item-label>
            <q-item-label caption>Information about spores &amp; poolen</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
export default {
  data () {
    return {
      leftDrawer: true
    }
  }
}
</script>
