<template>
  <div class="p-20 px-52">
    <div class="flex flex-col">
      <div class="flex overflow-hidden rounded-t-md bg-[#1e293b] border p-2">
        <ul class="flex w-full items-center justify-between list-none p-0">
          <li class="mr-2">
            <p class="font-bold text-2xl"> Uits Unix Lab</p>
          </li>
          <li>
            <button class="bg-red-600 px-4 py-2 rounded-md" @click="logOut"> Logout</button>
          </li>
        </ul>
      </div>
      <div>
        <div class="text-white">
          <LabTerminal :container-id="ddd" :status="false"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useAuthStore} from "~/store/auth.js";

const authStore = useAuthStore()
const router = useRouter()
const logOut = async () => {
  console.log("clicked")
  await authStore.logout()
  router.push("/login")
}

</script>

<style scoped>
/* Tailwind classes replace custom CSS */
</style>


<!--<template>-->
<!--  <div class="p-20 px-52">-->
<!--    <div class="flex flex-col">-->
<!--      <div class="flex overflow-hidden rounded-t-md bg-[#1e293b] border p-2">-->
<!--        <ul class="flex w-full items-center justify-between list-none">-->
<!--          <li class="mr-2 px-4 flex justify-center items-center space-x-3">-->
<!--            <p class="font-bold text-2xl"> UITS Unix Lab</p>-->
<!--          </li>-->
<!--          <li class="px-4 flex space-x-6">-->
<!--            <div class="text-sm">-->
<!--              <p>DNS Port: {{container_data.dnsPort}} </p>-->
<!--              <p>Web Address: {{ container_data.webPort}}</p>-->
<!--            </div>-->
<!--            <button class="bg-red-600 px-4 py-2 font-bold rounded-md" @click="logOut"> Logout</button>-->
<!--          </li>-->
<!--        </ul>-->
<!--      </div>-->
<!--      <div>-->
<!--        <UProgress v-if="status === 'loading'" size="xs" color="red"/>-->
<!--        <div class="h-[98%] w-100 border-x border-b -mt-1 pt-2 rounded-md">-->
<!--          <LabTerminal v-if="status==='success'" :container-id="container_data.containerId" />-->
<!--          <div v-if="status ==='error'"  class="w-full h-[70vh]">-->
<!--            <p class="px-4 text-red-500 text-sm"> An error occurred</p>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->