import { ref } from 'vue'

import { ItemType } from '@/types/Item'
import useItemStore from '@/stores/ItemStore'

export const useFormDialog = <T>(emits: any) => {
  const dialog = ref(false)
  const valid = ref(false)
  const form_data = ref<T>({} as T)
  const form_ref = ref()

  const rules = {
    required: (value: string) => !!value || 'Required field',
    alphanumeric: (value: string) =>
      /^[a-zA-Z0-9]+$/.test(value) || 'Please use alphanumeric characters only',
    numeric: (value: string) => /^[0-9]+$/.test(value) || 'Please use numbers only',
    username: (value: string) =>
      /^[a-zA-Z0-9\-_. \u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+$/.test(value) ||
      'Only letters, numbers, hyphens, underscores, dots, and spaces are allowed',
    password: (value: string) =>
      /^[a-zA-Z0-9\-_.]+$/.test(value) ||
      'Only letters, numbers, hyphens, underscores, and dots are allowed'
  }

  const submitData = () => {
    if (form_ref.value?.validate()) {
      emits('submit', form_data.value)
      dialog.value = false
    }
  }

  const deleteData = () => {
    emits('delete', form_data.value)
    dialog.value = false
  }

  return {
    dialog,
    valid,
    form_data,
    form_ref,
    rules,
    submitData,
    deleteData
  }
}

export const getDateRange = async (type: ItemType, rid_parent: number) => {
  if (rid_parent == undefined) {
    return null
  }

  const store_item = useItemStore()
  const item = await store_item.getParentItem(rid_parent)
  if (item.length == 0) {
    return null
  }

  let result: [string, string] = ['', '']
  switch (type) {
    case ItemType.EVENT:
      result = [item[0].project_datetime_start, item[0].project_datetime_end]
      break
    case ItemType.STORY:
      result = [item[0].project_datetime_start, item[1].event_datetime_end]
      break
  }
  return result
}
