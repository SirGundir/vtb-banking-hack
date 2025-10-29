import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useDebounceFn } from '@vueuse/core'

export const useResize = (handler?: () => void) => {
  const vh = ref(0)

  const setVh = () => {
    vh.value = window.innerHeight * 0.01

    document.documentElement.style.setProperty('--vh', `${vh.value}px`)
  }

  const debounced = useDebounceFn(() => {
    setVh()

    if (typeof handler === 'function') {
      handler()
    }
  }, 100)

  onMounted(() => {
    setVh()

    window.addEventListener('resize', debounced)
  })
  onBeforeUnmount(() => {
    window.removeEventListener('resize', debounced)
  })

  return {
    vh,
  }
}
