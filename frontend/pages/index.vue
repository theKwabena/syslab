

<template>
  <div class="px-2 m:p-4 sm:p-10 md:p-20 lg:px-52">
    <div class="flex flex-col">
      <div>
        <nav class="fixed top-0 left-0 z-10 right-0 bg-gray-800 text-white py-3 sm:hidden">
          <div class="px-4 flex items-center justify-between">
            <div class="flex justify-center items-center space-x-1">
              <UIcon name="i-heroicons-server-stack"/>
              <p class="font-bold">syslab.</p>
            </div>
            <div class="space-x-3 items-center flex">
              <UPopover>
                <UIcon name="i-heroicons-information-circle-16-solid" />
                <template #panel>
                  <div class="p-4 bg-[#1e293b]">
                    <p class="font-bold text-sm"> DNS Port: {{ container_data?.dnsPort }}</p>
                    <p class="font-bold text-sm"> Web Address: {{ container_data?.webPort }}</p>
                  </div>
                </template>
              </UPopover>
              <UButton color="red" size="xs" variant="outline" @click="logOut"> logout </UButton>
            </div>
          </div>
        </nav>
      </div>
      <div class="hidden md:flex flex-col md:flex-row overflow-hidden rounded-t-md bg-[#1e293b] border p-4 md:p-2">
        <ul class="flex w-full items-center justify-between list-none">
          <li class="mb-2 md:mb-0 md:mr-2 px-4 flex justify-center items-center space-x-3">
            <p class="font-bold text-xl md:text-2xl">💻syslab.</p>
          </li>
          <li class="flex flex-col md:flex-row items-start md:items-center space-y-2 md:space-y-0 md:space-x-6">
            <div class="text-sm flex space-x-3" v-if="container_data !== null">
              <p>DNS Port: {{ container_data?.dnsPort }}</p>
              <p>Web Address: {{ container_data?.webPort }}</p>
            </div>
            <UButton color="red" size="xs" variant="solid" @click="logOut"> logout </UButton>
          </li>
        </ul>
      </div>
      <div>
        <UProgress  v-if="status === 'loading'" size="xs" color="red" />
        <div class="pt-16 lg:pt-2 md:pt-0 h-screen md:h-[98%] lg:h-[70vh] w-full lg:border-x lg:border-b m:border-b m:border-x -mt-1 py-2">
          <LabTerminal v-if="status === 'success'" :container-id="container_data.containerId" />
          <div v-if="status === 'error'" class="w-full h-[70vh] border-x border-b flex items-center justify-center">
            <p class="text-red-500 text-sm">An error occurred</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useAuthStore} from "~/store/auth.ts";


const router = useRouter()
const authStore = useAuthStore()
const authToken = useCookie('token')
const config = useRuntimeConfig()

const {data, status, error} = await useFetch(`${config.public.BACKEND_URL}/me/container`,{
  headers: { Authorization: `Bearer ${authToken.value}` }
})


const container_data = computed(() => {
  if (!data.value) return null;

  return {
    id: data.value.id,
    dnsPort: data.value.dns_port,
    webPort: data.value.web_port,
    hostName: data.value.host_name,
    containerId: data.value.container_id,
    containerName: data.value.container_name,
  };
})



const logOut = async () => {
  await authStore.logout()
  router.push("/login")
}


</script>

<style scoped>
/* Tailwind classes replace custom CSS */
</style>
