<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { ExtractType, type Project } from '@/types/Item'

import useCommonStore from '@/stores/CommonStore'
import useUserStore from '@/stores/UserStore'
import useItemStore from '@/stores/ItemStore'
import useProjectStore from '@/stores/ProjectStore'
import LoginUser from '@/components/common/LoginUser.vue'
import SelectProjectDialog from '@/components/dialog/SelectProjectDialog.vue'
import SearchDialog from '@/components/dialog/SearchDialog.vue'

const TITLE_GLITCH = 'Glitch'

const title = ref(TITLE_GLITCH)

const route = useRoute()
const store_common = useCommonStore()
const store_user = useUserStore()
const store_item = useItemStore()
const store_project = useProjectStore()

const link_disabled = ref(true)
const link_project = ref('/')
const link_progress = ref('/')
const link_analyze = ref('/')

const dialog_project = ref()
const dialog_search = ref()

onMounted(async () => {
  await store_project.fetchProjects()
  common()
})

watch(
  () => store_common.mode,
  () => {
    common()
  }
)

const openProjectDialog = () => {
  dialog_project.value?.open()
}

const openSearchDialog = () => {
  dialog_search.value?.open()
}

const handleSubmitProject = async (id_project: number) => {
  if (id_project == 0) {
    dialog_project.value?.close()
    return
  }

  common()
  dialog_project.value?.close()
}

const common = () => {
  if (!store_common.isModeHome()) {
    title.value =
      store_project.projects.find(
        (project: Project) => project.rid == store_project.selected_id_project
      )?.title || TITLE_GLITCH
  } else {
    title.value = TITLE_GLITCH
  }

  link_project.value = '/project/' + store_project.selected_id_project
  link_progress.value =
    '/progress/' + store_project.selected_id_project + '/' + store_user.login_user?.rid
  link_analyze.value = '/analyze/' + store_project.selected_id_project

  if (store_user.login_user && store_project.selected_id_project) {
    link_disabled.value = false

    switch (Number(route.query.extruct)) {
      case ExtractType.ALL:
        store_item.setExtractAll()
        break
      case ExtractType.INCOMPLETE:
        store_item.setExtractIncomplete()
        break
      case ExtractType.HIGH_RISK:
        store_item.setExtractHighRisk()
        break
      case ExtractType.ALERT:
        store_item.setExtractAlert()
        break
      case ExtractType.ASSIGNMENT:
        store_item.setExtractAssignment()
        break
      case ExtractType.RELATION:
        store_item.setExtractItem(Number(route.query.target))
        break
      case ExtractType.SEARCH:
        store_item.setExtractSearch(String(route.query.target))
        break
    }
  }
}
</script>

<template>
  <v-app-bar color="#000000">
    <template v-slot:image>
      <v-img gradient="to top, rgba(0, 0, 0, 0), rgba(29, 35, 46, 0.4), rgba(106, 113, 124, 0.7)" />
    </template>

    <v-app-bar-title @click="openProjectDialog">
      <div class="d-flex align-center">
        <v-icon color="primary" size="small">mdi-grain</v-icon>
        <span class="ml-2">
          {{ title }}
        </span>
      </div>
    </v-app-bar-title>

    <v-btn icon>
      <router-link to="/">
        <v-icon color="icon">mdi-home</v-icon>
      </router-link>
    </v-btn>

    <v-btn icon :disabled="link_disabled" @click="store_item.setExtractIncomplete">
      <router-link :to="link_project">
        <v-icon color="icon">mdi-view-list</v-icon>
      </router-link>
    </v-btn>

    <v-btn icon :disabled="link_disabled">
      <router-link :to="link_progress">
        <v-icon color="icon">mdi-account-tag</v-icon>
      </router-link>
    </v-btn>

    <v-btn icon :disabled="link_disabled">
      <router-link :to="link_analyze">
        <v-icon color="icon">mdi-chart-scatter-plot-hexbin</v-icon>
      </router-link>
    </v-btn>

    <v-spacer />

    <div class="mr-3">
      <LoginUser />
    </div>

    <v-btn icon :disabled="link_disabled" @click="openSearchDialog">
      <v-icon color="icon">mdi-magnify</v-icon>
    </v-btn>

    <v-btn icon>
      <router-link to="/setting/main">
        <v-icon color="icon">mdi-cog</v-icon>
      </router-link>
    </v-btn>
  </v-app-bar>

  <SelectProjectDialog ref="dialog_project" @submit="handleSubmitProject" />
  <SearchDialog ref="dialog_search" />
</template>

<style scoped></style>
