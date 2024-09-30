<script setup lang="ts">
import { z } from 'zod'
import { useAuthStore } from '~/store/auth';
import type { FormError, FormSubmitEvent } from '#ui/types'

const form = ref()
const router = useRouter()
const authStore = useAuthStore()

const schema = z.object({
  username: z.string().min(3, { message: "Username must be at least 3 characters long" }),
  password: z.string()
})

type Schema = z.output<typeof schema>

const state = reactive({
  username: undefined,
  password: undefined
})


async function onSubmit (event: FormSubmitEvent<Schema>) {
    authStore.reset()
    await authStore.login(event.data)

    if(authStore.isAuthenticated){
      await router.push("/")
    }
}





</script>

<template>
  <div class="grid px-10 md:px-0 lg:px-0 md:grid-cols-12 lg:grid-cols-12 content-center h-screen">
      <div class="col-start-6 col-span-2 space-y-8">
        <div class="space-y-4">
          <p class="text-3xl font-semibold">💻</p>
          <p class="text-4xl font-semibold">Welcome to UITS syslab.</p>
        </div>
        <UForm ref="form" :schema="schema" :state="state" @submit="onSubmit" class="space-y-4">
          <p class="text-sm"> Enter username and password</p>
          <p v-if="authStore.isError.status" class="text-sm text-red-500"> {{ authStore.isError.message}}</p>
          <UFormGroup name="username">
            <UInput v-model="state.username" />
          </UFormGroup>

          <UFormGroup name="password">
            <UInput v-model="state.password" type="password" />
          </UFormGroup>

          <UButton type="submit" block color="red">
            <p class="font-bold">Submit</p>
          </UButton>
          <UProgress v-if="authStore.isLoading" animation="carousel" color="red"/>
        </UForm>
      </div>
    </div>
    <div>
  </div>

</template>

