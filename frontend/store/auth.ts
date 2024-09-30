import { defineStore } from 'pinia';
import {react} from "@babel/types";

import {useRuntimeConfig} from "#app";


interface UserPayloadInterface {
    username: string;
    password: string;
}

export const useAuthStore = defineStore('auth', ()=> {
    const config = useRuntimeConfig()
    const data = ref('')
    const isAuthenticated = ref(false);
    const isError = reactive({
        status: false,
        message: '',
    })
    const isLoading = ref(false)
    const isStatus = ref('')
    async function login({username, password}: UserPayloadInterface){
        const payload = new FormData();
        isLoading.value = true
        payload.append('username', username)
        payload.append('password', password)
        const {data, clear, error, status }: any = await useFetch(`${config.public.BACKEND_URL}/login/access-token`, {
            method: 'POST',
            body: payload,
            server: false
        })
        console.log(data.value, error.value, status.value)
        if (status.value == 'success'){
            isLoading.value = false
            const token = useCookie('token')
            token.value = data?.value?.access_token;
            isAuthenticated.value = true
        }
        else if(status.value == 'error'){
            isLoading.value = false
            isError.status = true
            if(error.value.data){
                isError.message = error.value.data.detail
            } else if(error.value.statusMessage != null){
                isError.message = error.value.statusMessage

            } else {
                isError.message = `An error occurred, Status: ${error.value.statusCode}`
            }
            console.log(isError.status)
        }
        isLoading.value = false
    }

    function reset() {
        isError.status = false
        isError.message = ''
    }

    async function logout(){
        const token = useCookie('token')
        isAuthenticated.value = false
        token.value = null
    }

    return {login, isAuthenticated, isError, reset, logout, isLoading}
});