<script setup lang="ts">
import type { UserCreate } from '@/types/User'
import { useFormDialog } from '@/components/dialog/BaseDialog'

const emit = defineEmits(['submit'])
const { dialog, valid, form_data, form_ref, rules, submitData } = useFormDialog<UserCreate>(emit)

defineExpose({
  open() {
    dialog.value = true
    form_data.value = {
      user: '',
      password: '',
      name: '',
      is_admin: 1
    }
  },
  close() {
    dialog.value = false
  }
})
</script>

<template>
  <v-dialog v-model="dialog" max-width="600px" persistent>
    <v-card>
      <v-card-title>
        <span class="dialog-title">Add Administrator</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <v-text-field
            v-model="form_data.user"
            :rules="[rules.required, rules.alphanumeric]"
            label="User"
            autocomplete="current-user"
            required
          />

          <v-text-field
            v-model="form_data.password"
            :rules="[rules.required, rules.password]"
            label="Password"
            type="password"
            autocomplete="current-password"
            required
          />

          <v-text-field
            v-model="form_data.name"
            :rules="[rules.required, rules.username]"
            label="Name"
            required
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
