<template>
  <q-layout view="hHh lpR fFf">

    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="leftDrawer = !leftDrawer" />

        <q-toolbar-title>
          Pollen/Spores - Luxembourg
        </q-toolbar-title>

        <q-select
          v-model="lang"
          :options="langOptions"
          label="Language"
          dense
          borderless
          emit-value
          map-options
          options-dense
          style="min-width: 150px"
          />
      </q-toolbar>
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
      <router-view :proxy="proxy"/>
    </q-page-container>

  </q-layout>
</template>

<script>
import { Proxy } from 'src/proxy.js'

function getLanguage (proxy) {
  return proxy.getSupportedLanguages()
    .then(supportedLanguages => {
      let browserSetting = navigator.languages || [navigator.language]
      let bestMatch = ''
      browserSetting.forEach(item => {
        let langCode = item.split('-')[0]
        if (supportedLanguages.indexOf(langCode) > -1 && bestMatch === '') {
          bestMatch = langCode
        }
      })
      return bestMatch
    })
}

export default {
  data () {
    return {
      leftDrawer: false,
      proxy: new Proxy('http://localhost:5000'),
      lang: this.$i18n.locale,
      langOptions: [
        { value: 'en', label: 'English' },
        { value: 'de', label: 'Deutsch' },
        { value: 'fr', label: 'Français' },
        { value: 'lb', label: 'Lëtzebuergesch' }
      ]
    }
  },
  watch: {
    lang (lang) {
      this.$i18n.locale = lang
    }
  },
  created () {
    getLanguage(this.proxy).then(value => {
      this.lang = value
    })
  }
}
</script>
