import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './styles/main.css'
import AppButton from './components/ui/AppButton.vue'
import AppInput from './components/ui/AppInput.vue'
import AppLabel from './components/ui/AppLabel.vue'
import AppSelect from './components/ui/AppSelect.vue'

const app = createApp(App)
app.use(createPinia())
app.use(router)

app.component('AppButton', AppButton)
app.component('AppInput', AppInput)
app.component('AppLabel', AppLabel)
app.component('AppSelect', AppSelect)

app.mount('#app')
