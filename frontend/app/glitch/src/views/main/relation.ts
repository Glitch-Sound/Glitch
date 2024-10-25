import { ItemType, type Item, type PanelRelation } from '@/types/Item'

const getParentType = (type: ItemType): ItemType | null => {
  switch (type) {
    case ItemType.EVENT:
      return ItemType.PROJECT
    case ItemType.FEATURE:
      return ItemType.EVENT
    case ItemType.STORY:
      return ItemType.FEATURE
    case ItemType.TASK:
      return ItemType.STORY
    case ItemType.BUG:
      return ItemType.TASK
    default:
      return null
  }
}

const getChildType = (type: ItemType): ItemType | null => {
  switch (type) {
    case ItemType.EVENT:
      return ItemType.FEATURE
    case ItemType.FEATURE:
      return ItemType.STORY
    case ItemType.STORY:
      return ItemType.TASK
    case ItemType.TASK:
      return ItemType.BUG
    default:
      return null
  }
}

const getTypeLevel = (type: ItemType): number => {
  switch (type) {
    case ItemType.EVENT:
      return 0
    case ItemType.FEATURE:
      return 1
    case ItemType.STORY:
      return 2
    case ItemType.TASK:
      return 3
    case ItemType.BUG:
      return 4
    default:
      return -1
  }
}

const findNextTypeIndexAfter = (items: Item[], startIndex: number, type: ItemType): number => {
  const nextIndex = items.slice(startIndex + 1).findIndex((item) => item.type === type)
  return nextIndex !== -1 ? startIndex + 1 + nextIndex : -1
}

const findNextTypesIndexAfter = (items: Item[], startIndex: number, types: ItemType[]): number => {
  const slice = items.slice(startIndex + 1)
  for (let i = 0; i < slice.length; i++) {
    if (types.includes(slice[i].type)) {
      return startIndex + 1 + i
    }
  }
  return -1
}

export const getPanelRelation = (items: Item[], index: number): PanelRelation => {
  const type_current = items[index].type
  const type_next = items[index + 1]?.type

  const parent_type = getParentType(type_current)
  const child_type = getChildType(type_current)

  const previous_item = items[index - 1]
  const previous_type = previous_item?.type

  const next_same_type_index = findNextTypeIndexAfter(items, index, type_current)

  let condition1 = false
  if (next_same_type_index !== -1) {
    const has_parent_in_between =
      parent_type !== null &&
      items.slice(index + 1, next_same_type_index).some((item) => item.type === parent_type)
    condition1 = !has_parent_in_between && previous_type !== type_current
  }

  const condition2 = previous_type !== type_current && previous_type === parent_type

  const is_last_item = index === items.length - 1
  const parent_type_level =
    parent_type !== null ? getTypeLevel(parent_type) : getTypeLevel(type_current) - 1
  const next_type_level = type_next !== undefined ? getTypeLevel(type_next) : Infinity
  const is_next_higher_or_parent = next_type_level <= parent_type_level

  // is_top.
  let is_top = false
  is_top = condition1 || condition2

  // is_bottom.
  let is_bottom = is_last_item || is_next_higher_or_parent
  if (type_current === ItemType.TASK && type_next === ItemType.BUG) {
    is_bottom = true
  }

  // has_child.
  const has_child = type_next === child_type

  // is_exist_next_event.
  const is_exist_next_event = findNextTypeIndexAfter(items, index, ItemType.EVENT) !== -1

  // is_exist_next_feature.
  const next_feature_index = findNextTypeIndexAfter(items, index, ItemType.FEATURE)
  let is_exist_next_feature = false
  if (next_feature_index !== -1) {
    const parent_of_feature = getParentType(ItemType.FEATURE)
    const has_parent_in_between =
      parent_of_feature !== null &&
      items.slice(index + 1, next_feature_index).some((item) => item.type === parent_of_feature)
    is_exist_next_feature = !has_parent_in_between
  }

  // is_exist_next_story.
  const next_story_index = findNextTypeIndexAfter(items, index, ItemType.STORY)
  let is_exist_next_story = false
  if (next_story_index !== -1) {
    const parent_of_story = getParentType(ItemType.STORY)
    const has_parent_in_between =
      parent_of_story !== null &&
      items.slice(index + 1, next_story_index).some((item) => item.type === parent_of_story)
    is_exist_next_story = !has_parent_in_between
  }

  // is_exist_next_task_bug.
  const next_task_bug_index = findNextTypesIndexAfter(items, index, [ItemType.TASK, ItemType.BUG])
  let is_exist_next_task_bug = false
  if (next_task_bug_index !== -1) {
    const parent_of_task = getParentType(ItemType.TASK)
    const has_parent_in_between =
      parent_of_task !== null &&
      items.slice(index + 1, next_task_bug_index).some((item) => item.type === parent_of_task)
    is_exist_next_task_bug = !has_parent_in_between
  }

  // console.log('type_current           : ' + type_current)
  // console.log('is_top                 : ' + is_top)
  // console.log('is_bottom              : ' + is_bottom)
  // console.log('has_child              : ' + has_child)
  // console.log('is_exist_next_event    : ' + is_exist_next_event)
  // console.log('is_exist_next_feature  : ' + is_exist_next_feature)
  // console.log('is_exist_next_story    : ' + is_exist_next_story)
  // console.log('is_exist_next_task_bug : ' + is_exist_next_task_bug)

  return {
    is_top,
    is_bottom,
    has_child,
    is_exist_next_event,
    is_exist_next_feature,
    is_exist_next_story,
    is_exist_next_task_bug
  }
}
