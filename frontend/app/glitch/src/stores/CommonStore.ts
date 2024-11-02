import { defineStore } from 'pinia'

enum Mode {
  NONE = 0,
  PROJECT,
  PROGRESS,
  ANALYZE
}

const useCommonStore = defineStore('common', {
  state: () => ({
    mode: Mode.PROJECT as Mode
  }),
  actions: {
    setModeProject() {
      this.mode = Mode.PROJECT
    },
    setModeProgress() {
      this.mode = Mode.PROGRESS
    },
    setModeAnalyze() {
      this.mode = Mode.ANALYZE
    },
    isModeProject() {
      return this.mode == Mode.PROJECT
    },
    isModeProgress() {
      return this.mode == Mode.PROGRESS
    },
    isModeAnalyze() {
      return this.mode == Mode.ANALYZE
    }
  }
})

export default useCommonStore
