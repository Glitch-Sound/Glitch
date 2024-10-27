<script setup lang="ts">
import { onMounted, ref } from 'vue'

import type { Activity } from '@/types/Activity'

import useUserStore from '@/stores/UserStore'
import useItemStore from '@/stores/ItemStore'
import MarkedText from '@/components/common/MarkedText.vue'

const store_user = useUserStore()
const store_item = useItemStore()

const dialog = ref(false)
const rid_item = ref(0)
const comment = ref('')
const activities = ref<Activity[]>([])

defineExpose({
  open(target: number) {
    dialog.value = true
    rid_item.value = target
  },
  close() {
    dialog.value = false
  }
})

onMounted(async () => {
  activities.value = await store_item.getActivities(rid_item.value)
})

const addComment = async () => {
  if (store_user.login_user && comment.value.trim()) {
    await store_item.createActivity({
      rid_items: rid_item.value,
      rid_users: store_user.login_user.rid,
      activity: comment.value
    })

    activities.value = await store_item.getActivities(rid_item.value)
    comment.value = ''
  }
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="1300px">
    <v-card>
      <v-card-title>
        <span class="text-h5">Activity</span>
      </v-card-title>

      <v-card-text>
        <div v-for="activity in activities" :key="activity.rid" class="mb-5">
          <div class="user">
            <span>{{ activity.datetime_entry }}</span>
            <span class="mx-3">{{ activity.name }}</span>
          </div>
          <div><MarkedText :src="activity.activity" /></div>
        </div>

        <v-form class="mt-8">
          <v-textarea v-model="comment" required />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" :disabled="comment == ''" @click="addComment">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
.user {
  color: #696969;
  font-size: 0.9rem;
}
</style>
