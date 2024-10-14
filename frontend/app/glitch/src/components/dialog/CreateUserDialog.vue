<script setup lang="ts">
import { defineExpose } from 'vue'

import { useDialog } from '@/components/dialog/BaseDialog'
import type { UserCreate } from '@/types/User'

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, submitData } = useDialog<UserCreate>(emit)

defineExpose({
  open() {
    dialog.value = true
    form_data.value = {
      user: '',
      password: '',
      name: '',
      is_admin: 0
    }
  },
  close() {
    dialog.value = false
  }
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Add User</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <v-text-field
            v-model="form_data.user"
            :rules="[rules.required, rules.alphanumeric]"
            label="User"
            required
          />

          <v-text-field
            v-model="form_data.password"
            :rules="[rules.required, rules.password]"
            label="Password"
            type="password"
            required
          />

          <v-text-field
            v-model="form_data.name"
            :rules="[rules.required, rules.username]"
            label="Name"
            required
          />

          <v-checkbox
            v-model="form_data.is_admin"
            color="checkbox"
            :true-value="1"
            :false-value="0"
            label="Is Admin"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="submitData">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';
</style>
