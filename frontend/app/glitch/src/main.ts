import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from '@/router'

import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import { createVuetify, type ThemeDefinition } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import WebFont from 'webfontloader'

const app = createApp(App)
const pinia = createPinia()

WebFont.load({
  google: {
    families: ['Noto+Sans+JP:wght@100..900&display=swap']
  }
})

const theme_dark: ThemeDefinition = {
  dark: true,
  colors: {
    background: '#000000',
    surface: '#000000',
    onSurface: '#f0f0f0',
    primary: '#2196f3',
    icon: '#e0e0e0',
    addButton: '#940000',
    checkbox: '#cfcfcf'
  },
  variables: {
    fontFamily: 'Noto Sans JP, sans-serif'
  }
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'theme_dark',
    themes: {
      theme_dark
    }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi
    }
  }
})

app.use(pinia)
app.use(router)
app.use(vuetify)

app.mount('#app')
