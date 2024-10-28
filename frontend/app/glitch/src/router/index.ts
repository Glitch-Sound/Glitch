import { createRouter, createWebHistory } from 'vue-router'

import MainView from '@/views/MainView.vue'
import ProjectView from '@/views/main/ProjectView.vue'
import ProgressView from '@/views/main/ProgressView.vue'
import AnalyzeView from '@/views/main/AnalyzeView.vue'

import SettingMainView from '@/views/setting/SettingMainView.vue'
import SettingUserView from '@/views/setting/SettingUserView.vue'
import SettingProjectView from '@/views/setting/SettingProjectView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainView
    },
    {
      path: '/project/:id_project/:extruct?/:target?',
      component: ProjectView,
      meta: { requiresAuth: true }
    },
    {
      path: '/progress/:id_project/:target',
      component: ProgressView,
      meta: { requiresAuth: true }
    },
    {
      path: '/analyze/:id_project',
      component: AnalyzeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/setting',
      children: [
        {
          path: 'main',
          component: SettingMainView
        },
        {
          path: 'user',
          component: SettingUserView
        },
        {
          path: 'project',
          component: SettingProjectView
        }
      ],
      meta: { requiresAuth: true }
    }
  ]
})

export default router
