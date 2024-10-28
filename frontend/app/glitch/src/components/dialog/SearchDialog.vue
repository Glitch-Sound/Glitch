<script setup lang="ts">
import { ref } from 'vue'

import useItemStore from '@/stores/ItemStore'

const store_item = useItemStore()

defineExpose({
  open() {
    dialog.value = true
  },
  close() {
    dialog.value = false
  }
})

const dialog = ref(false)
const target = ref('')

const search = () => {
  store_item.setExtractSearch(target.value)
  dialog.value = false
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="1000px">
    <v-card>
      <v-card-title>
        <span class="text-h5">Search</span>
      </v-card-title>

      <v-card-text>
        <v-form>
          <v-text-field v-model="target" label="Target" required />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" @click="search">Search</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
