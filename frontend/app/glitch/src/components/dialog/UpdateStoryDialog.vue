<script setup lang="ts">
import { defineExpose, onMounted, ref } from 'vue'

import { ItemType, ItemState, type StoryUpdate } from '@/types/Item'
import type { User } from '@/types/User'
import { useFormDialog, getDateRange } from '@/components/dialog/BaseDialog'

import DeleteButton from '@/components/common/DeleteButton.vue'
import StateSelect from '@/components/common/StateSelect.vue'
import UserSelect from '@/components/common/UserSelect.vue'

const date_min = ref('')
const date_max = ref('')

const emit = defineEmits(['submit', 'delete'])
const { dialog, valid, form_data, form_ref, rules, submitData, deleteData } =
  useFormDialog<StoryUpdate>(emit)

defineExpose({
  open(data: StoryUpdate) {
    dialog.value = true
    form_data.value = { ...data }
  },
  close() {
    dialog.value = false
  }
})

onMounted(async () => {
  const range = await getDateRange(ItemType.STORY)
  if (range) {
    ;[date_min.value, date_max.value] = range
  }
})

const handleUserSelected = (user: User) => {
  form_data.value.rid_users = user.rid
}

const handleStateSelected = (state: ItemState) => {
  form_data.value.state = state
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="1300px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Update Story</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="form_ref" v-model="valid" lazy-validation>
          <UserSelect v-model="form_data.rid_users" @itemSelected="handleUserSelected" />

          <StateSelect
            :type="ItemType.PROJECT"
            :state="form_data.state"
            @itemSelected="handleStateSelected"
          />

          <v-text-field
            v-model="form_data.title"
            :rules="[rules.required]"
            label="Title"
            required
          />

          <v-textarea v-model="form_data.detail" label="Detail" />
          <v-textarea v-model="form_data.result" label="Result" />

          <v-text-field
            v-model="form_data.story_datetime_start"
            :rules="[rules.required]"
            label="Start"
            type="date"
            required
            :min="date_min"
            :max="date_max"
          />

          <v-text-field
            v-model="form_data.story_datetime_end"
            :rules="[rules.required]"
            label="End"
            type="date"
            required
            :min="date_min"
            :max="date_max"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <DeleteButton @delete="deleteData" />
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
