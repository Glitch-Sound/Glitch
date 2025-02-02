<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { type Project } from '@/types/Item'
import type { MemberCreate } from '@/types/User'
import { useNoFormDialog } from '@/components/dialog/BaseDialog'
import useUserStore from '@/stores/UserStore'

const store_user = useUserStore()

const project = ref<Project | null>(null)
const selected_user = ref<any>(null)
const selected_member = ref<any>(null)

const emit = defineEmits(['submit', 'delete'])
const { dialog, return_data, submitData } = useNoFormDialog<MemberCreate[]>(emit)

defineExpose({
  open(data: Project) {
    dialog.value = true
    project.value = data
    store_user.fetchMembers(data.id_project)
  },
  close() {
    dialog.value = false
  }
})

onMounted(async () => {
  store_user.fetchUsers()
})

// 右側の Member リストは、active が false のユーザのみを表示
const memberList = computed(() => {
  return store_user.users.filter((u: any) => u.active === false)
})

// 左側はすべてのユーザを表示（active === false の場合 disable 状態にする）

function selectUser(user: any) {
  // すでに非活性の場合は選択できない
  if (user.active === false) return
  selected_user.value = user
  selected_member.value = null
}

function selectMember(user: any) {
  // すでに active なユーザは選択できない
  if (user.active !== false) return
  selected_member.value = user
  selected_user.value = null
}

/**
 * 右ボタン押下時の処理
 * 選択した User の active を false にして、disable 状態にする（Member に追加）
 */
function addToMembers() {
  if (!selected_user.value) return

  // User 側は削除せず、disable 状態にする
  selected_user.value.active = false

  // API 更新などが必要な場合はここで実施

  selected_user.value = null
}

/**
 * 左ボタン押下時の処理
 * 選択した Member の active を true に戻して、User 側の disable 状態を解除する
 */
function removeFromMembers() {
  if (!selected_member.value) return

  selected_member.value.active = true

  // API 更新などが必要な場合はここで実施

  selected_member.value = null
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="1300px">
    <v-card>
      <v-card-title>
        <span class="dialog-title">Member</span>
      </v-card-title>

      <v-card-text>
        <v-row>
          <!-- 左側: User 一覧（すべてのユーザを表示、active=false の場合 disable 状態にする） -->
          <v-col cols="5">
            <div class="text-h6 mb-2">User</div>
            <v-list>
              <v-list-item
                v-for="user in store_user.users"
                :key="user.rid"
                @click="user.active !== false && selectUser(user)"
                :disabled="user.active === false"
                :class="{ 'selected-item': selected_user && selected_user.rid === user.rid }"
              >
                <v-list-item-title>{{ user.name }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-col>

          <!-- 中央: 移動用ボタン -->
          <v-col cols="2" class="d-flex flex-column justify-center align-center">
            <!-- 右向きボタン：User → Member -->
            <v-btn icon color="primary" @click="addToMembers" :disabled="!selected_user">
              <v-icon>mdi-arrow-right</v-icon>
            </v-btn>
            <!-- 左向きボタン：Member → User -->
            <v-btn icon color="primary" @click="removeFromMembers" :disabled="!selected_member">
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
          </v-col>

          <!-- 右側: Member 一覧（active=false のユーザのみ） -->
          <v-col cols="5">
            <div class="text-h6 mb-2">Member</div>
            <v-list>
              <v-list-item
                v-for="user in memberList"
                :key="user.rid"
                @click="selectMember(user)"
                :class="{ 'selected-item': selected_member && selected_member.rid === user.rid }"
              >
                <v-list-item-title>{{ user.name }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="dialog = false">Cancel</v-btn>
        <v-btn color="primary" @click="submitData">Submit</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
@import '@/assets/main.css';

/* 選択中の項目にハイライト */
.selected-item {
  background-color: rgba(0, 0, 255, 0.1);
}
</style>
