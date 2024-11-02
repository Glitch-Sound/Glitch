import { defineStore } from 'pinia'

enum Mode {
  HOME = 0,
  PROJECT,
  PROGRESS,
  ANALYZE
}

const useCommonStore = defineStore('common', {
  state: () => ({
    mode: Mode.HOME as Mode
  }),
  actions: {
    setModeHome() {
      this.mode = Mode.HOME
    },
    setModeProject() {
      this.mode = Mode.PROJECT
    },
    setModeProgress() {
      this.mode = Mode.PROGRESS
    },
    setModeAnalyze() {
      this.mode = Mode.ANALYZE
    },
    isModeHome() {
      return this.mode == Mode.HOME
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
