<script setup lang="ts">
import { ref, defineProps, watch } from 'vue'

import { ItemType, ItemState, type BugUpdate } from '@/types/Item'
import type { User } from '@/types/User'
import type { EmitDialog } from '@/components/common/events'
import { useDialog } from '@/components/dialog/BaseDialog'
import UserSelect from '@/components/common/UserSelect.vue'
import UserReviewSelect from '@/components/common/UserReviewSelect.vue'
import WorkloadSelect from '@/components/common/WorkloadSelect.vue'
import StateSelect from '@/components/common/StateSelect.vue'
import DeleteButton from '@/components/common/DeleteButton.vue'

const props = defineProps<{
  dialog_show: boolean
  data_form: BugUpdate
}>()

const is_review = ref(false)

const emit = defineEmits<EmitDialog>()
const { dialog, valid, data_form, ref_form, rules, submitData, deleteData } = useDialog(props, emit)

watch(
  () => data_form.value.state,
  (state_new) => {
    if (state_new == ItemState.REVIEW) {
      is_review.value = true
    } else {
      is_review.value = false
    }
  }
)

const handleUserSelected = (user: User) => {
  data_form.value.rid_users = user.rid
}

const handleUserReviewSelected = (user: User) => {
  data_form.value.rid_users_review = user.rid
}

const handleStateSelected = (state: ItemState) => {
  data_form.value.state = state
}

const handleWorkloadSelect = (workload: number) => {
  data_form.value.workload = workload
}
</script>

<template>
  <v-dialog v-model="dialog" class="panel-common">
    <v-card>
      <v-card-title>
        <span class="text-h5">Update Bug</span>
      </v-card-title>

      <v-card-text>
        <v-form ref="ref_form" v-model="valid" lazy-validation>
          <UserSelect v-model="data_form.rid_users" @itemSelected="handleUserSelected" />

          <UserReviewSelect
            v-if="is_review"
            :rules="[rules.required]"
            v-model="data_form.rid_users_review"
            @itemSelected="handleUserReviewSelected"
          />

          <StateSelect
            :type="ItemType.EVENT"
            :state="data_form.state"
            @itemSelected="handleStateSelected"
          />

          <v-text-field
            v-model="data_form.title"
            :rules="[rules.required]"
            label="Title"
            required
          />

          <v-textarea v-model="data_form.detail" label="Detail" />
          <v-textarea v-model="data_form.result" label="Result" />

          <WorkloadSelect :workload="data_form.workload" @itemSelected="handleWorkloadSelect" />
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
@import '@/components/dialog/dialog.css';
</style>
