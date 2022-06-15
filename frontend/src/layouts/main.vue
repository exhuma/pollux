<template>
  <q-layout view="hHh lpR fFf">

    <q-header reveal elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="leftDrawer = !leftDrawer" />
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawer"
      side="left"
      bordered
      content-class="bg-grey-2"
    >
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

export default {
  data () {
    return {
      leftDrawer: false,
      username: '',
      isPwd: true,
    }
  },
}
</script>
