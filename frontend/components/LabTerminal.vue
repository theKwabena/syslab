<script setup>
import { ref, onMounted, watch } from 'vue';
import { Terminal } from "@xterm/xterm";
import { AttachAddon } from "@xterm/addon-attach";
import '@xterm/xterm/css/xterm.css'
import { FitAddon } from '@xterm/addon-fit';


const config = useRuntimeConfig()
// Define the containerId as a prop
const props = defineProps({
  containerId: {
    type: String,
    required: true
  },
});

const terminal = new Terminal();
terminal.options.theme.background = "#0f172a";
const fitAddon = new FitAddon();

const container = ref(null);
const error = reactive({
  status: false,
  message: ''
})

function initTerminal() {
  if (!props.containerId) {
    console.error('Container ID is required');
    return;
  }

  const socket = new WebSocket(`ws://${config.public.DAEMON_URL}/containers/${props.containerId}/attach/ws?stream=1&stdout=1&stdin=1&logs=1`);
  socket.onerror = (event) => {
    error.status = true
    error.message = "Error Code D1001"
    console.log(event)
  }

  const attachAddon = new AttachAddon(socket);
  terminal.loadAddon(fitAddon);
  terminal.loadAddon(attachAddon);
  terminal.open(container.value);
  fitAddon.fit();
}

onMounted(initTerminal);

// Watch for changes in containerId and reinitialize the terminal
watch(() => props.containerId, () => {
  terminal.clear();
  initTerminal();
});
</script>


<template>
  <div class="w-full h-full m:h-[70vh]">
    <div ref="container" class="h-[100%] w-100">
      <p v-if="error.status" class="px-4 text-red-500 text-sm"> Error: Cannot get user environment: {{error.message}}</p>
    </div>

  </div>
</template>

<style scoped>

</style>
