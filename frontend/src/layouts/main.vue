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
        <q-btn v-if="token === ''" rounded flat @click="startLogin" icon="login" />
        <q-btn v-if="token !== ''" rounded flat @click="logout" icon="account_circle" />
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

        <q-item to="/data" exact>
          <q-item-section avatar>
            <q-icon name="archive" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Data Management</q-item-label>
            <q-item-label caption>Add new data to the backend</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>

      <q-dialog v-model="loginDialog" persistent>
        <q-card style="min-width: 350px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Login</div>
          </q-card-section>
          <q-card-section class="q-pt-none">
            <q-input label="Username" v-model="username" autofocus />
          </q-card-section>
          <q-card-section class="q-pt-none">
            <q-input
              label="Password"
              v-model="password"
              :type="isPwd ? 'password' : 'text'"
              @keyup.enter="acceptLogin">
              <template v-slot:append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                  />
              </template>
            </q-input>
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn flat label="Cancel" @click="cancelLogin" />
            <q-btn flat label="Login" @click="acceptLogin" />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <router-view
        @tokenChanged="onTokenChanged"
        :proxy="proxy"
        :locale="lang"
        />
    </q-page-container>

  </q-layout>
</template>

<script>
import { Proxy } from 'src/proxy'

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
      token: '',
      proxy: null,
      lang: this.$i18n.locale,
      loginDialog: false,
      username: '',
      password: '',
      isPwd: true,
      langOptions: [
        { value: 'en', label: 'English' },
        { value: 'de', label: 'Deutsch' },
        { value: 'fr', label: 'Français' },
        { value: 'lb', label: 'Lëtzebuergesch' }
      ]
    }
  },
  methods: {
    startLogin () {
      this.loginDialog = true
    },
    logout () {
      this.login = ''
      this.password = ''
      this.onTokenChanged('')
    },
    acceptLogin () {
      if (this.username && this.password) {
        this.proxy.login(this.username, this.password)
          .then(token => {
            this.onTokenChanged(token)
          })
      }
      this.password = ''
      this.loginDialog = false
    },
    cancelLogin () {
      this.login = ''
      this.password = ''
      this.loginDialog = false
    },
    onTokenChanged (token) {
      if (!token) {
        localStorage.removeItem('token')
        this.token = ''
        this.proxy.setToken('')
        return
      }
      localStorage.setItem('token', token)
      this.token = token
      this.proxy.setToken(token)
    }
  },
  watch: {
    lang (lang) {
      this.$i18n.locale = lang
    }
  },
  created () {
    this.token = localStorage.getItem('token') || ''
    this.proxy = new Proxy(process.env.VUE_POLLUX_API, this.token)
    getLanguage(this.proxy).then(value => {
      this.lang = value
    })
  }
}
</script>
